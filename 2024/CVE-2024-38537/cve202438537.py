import requests

def check_csp_for_polyfill(url):
    try:
        response = requests.head(url)
        csp_header = response.headers.get('Content-Security-Policy')
        
        if csp_header:
            if 'polyfill.io' in csp_header:
                print(f"polyfill.io is allowed in CSP header of {url}")
            else:
                print(f"polyfill.io is not allowed in CSP header of {url}")
        else:
            print(f"No Content-Security-Policy header found for {url}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching headers for {url}: {e}")

# Read URLs from a file
def read_urls_from_file(filename):
    with open(filename, 'r') as file:
        urls = file.read().splitlines()
    return urls

# Example usage
if __name__ == "__main__":
    filename = 'urls.txt'  # Replace with your file name
    urls = read_urls_from_file(filename)

    # Iterate over each URL and check CSP
    for url in urls:
        check_csp_for_polyfill(url)
