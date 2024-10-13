import ssl
import socket

# Function to check the OpenSSL version
def check_openssl_version():
    version = ssl.OPENSSL_VERSION
    print(f"OpenSSL Version: {version}")
    if "3.0.0" in version:
        print("Warning: Your OpenSSL version is 3.0.0, which is vulnerable to CVE-2021-4044.")
    else:
        print("Your OpenSSL version is not affected by CVE-2021-4044.")

# Function to test SSL error handling for a given website
def test_ssl_error_handling(website):
    try:
        # Remove http/https prefix if present
        website = website.replace("https://", "").replace("http://", "")
        
        # Simulate an SSL connection
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=website)
        conn.connect((website, 443))
        conn.do_handshake()
        print(f"SSL handshake with {website} completed successfully.")
        
    except ssl.SSLError as e:
        error_code = e.errno  # ssl.SSL_get_error isn't available in Python, but errno provides similar info
        print(f"SSL error occurred while connecting to {website}: {e}")
        if error_code:
            print(f"Error code: {error_code}")
    except Exception as e:
        print(f"An error occurred while connecting to {website}: {e}")

if __name__ == "__main__":
    # Get the website from the user
    website = input("Enter the website URL (e.g., example.com): ").strip()
    
    check_openssl_version()
    test_ssl_error_handling(website)

