import requests
import re
import os
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

def print_welcome_message():
    welcome_text = """
    /$$$$$$                                                    /$$       /$$$$$$$$                                     
   /$$__  $$                                                  | $$      |__  $$__/                                     
  | $$  \\ $$  /$$$$$$   /$$$$$$$  /$$$$$$  /$$$$$$$   /$$$$$$ | $$         | $$  /$$$$$$   /$$$$$$  /$$$$$$/$$$$       
  | $$$$$$$$ /$$__  $$ /$$_____/ /$$__  $$| $$__  $$ |____  $$| $$         | $$ /$$__  $$ |____  $$| $$_  $$_  $$      
  | $$__  $$| $$  \\__/|  $$$$$$ | $$$$$$$$| $$  \\ $$  /$$$$$$$| $$         | $$| $$$$$$$$  /$$$$$$$| $$ \\ $$ \\ $$      
  | $$  | $$| $$       \\____  $$| $$_____/| $$  | $$ /$$__  $$| $$         | $$| $$_____/ /$$__  $$| $$ | $$ | $$      
  | $$  | $$| $$       /$$$$$$$/|  $$$$$$$| $$  | $$|  $$$$$$$| $$         | $$|  $$$$$$$|  $$$$$$$| $$ | $$ | $$      
  |__/  |__/|__/      |_______/  \\_______/|__/  |__/ \\_______/|__/         |__/ \\_______/ \\_______/|__/ |__/ |__/      
    """
    
    print(Fore.RED + welcome_text)
    print(Fore.YELLOW + "Welcome to ZeroDayX PoC for CVE-2025-26909 - Arsenal Team")
    print(Style.RESET_ALL)

def check_vulnerability(base_url, output_file):
    url = f"{base_url}/wp-content/plugins/hide-my-wp/readme.txt"
    
    try:
        response = requests.get(url, allow_redirects=True)
        
        if response.status_code == 200:
            version_match = re.search(r"(?mi)Stable tag: ([0-9.]+)", response.text)
            if version_match:
                version = version_match.group(1)
                output = f"Target: {base_url} - Plugin version found: {version}\n"
                
                if version <= "5.4.01":
                    output += "Vulnerability exists: Unauthenticated Local File Inclusion is possible.\n"
                    print(Fore.GREEN + output)
                else:
                    output += "No vulnerability found: Plugin version is secure.\n"
                    print(Fore.YELLOW + output)
            else:
                output = f"Target: {base_url} - Version information not found in the readme.txt.\n"
                print(Fore.YELLOW + output)
        else:
            output = f"Target: {base_url} - Failed to retrieve the file. Status code: {response.status_code}\n"
            print(Fore.RED + output)
        
        with open(output_file, 'a') as f:
            f.write(output)
    
    except Exception as e:
        error_message = f"An error occurred while processing {base_url}: {e}\n"
        with open(output_file, 'a') as f:
            f.write(error_message)
        print(Fore.RED + error_message)

def main():
    print_welcome_message()
    
    num_threads = input("Enter the number of threads for requests (1 to 8, default is 4): ")
    num_threads = int(num_threads) if num_threads.isdigit() and 1 <= int(num_threads) <= 8 else 4
    
    input_file = input("Please enter the path to the file containing target URLs: ")
    
    if not os.path.isfile(input_file):
        print(Fore.RED + "The specified file does not exist. Please check the path and try again.")
        return
    
    output_file = "vulnerability_report.txt"
    
    with open(input_file, 'r') as f:
        targets = f.readlines()
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for target in targets:
            target = target.strip()
            if target:
                executor.submit(check_vulnerability, target, output_file)

if __name__ == "__main__":
    main()
