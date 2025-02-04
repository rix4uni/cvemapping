import requests

def check_for_datatables(url):
    try:
        response = requests.get(url)
        if 'datatables' in response.text:
            print("[+] DataTables found in the HTML.")
        else:
            print("[-] DataTables not found in the HTML.")
        
        # Optionally check known endpoints
        endpoints = ['/api/data', '/data', '/datatable']
        for endpoint in endpoints:
            res = requests.get(url + endpoint)
            if res.status_code == 200:
                print(f"[+] Found DataTables endpoint: {url + endpoint}")
    except requests.RequestException as e:
        print(f"[!] Error connecting to {url}: {e}")

if __name__ == "__main__":
    target_url = input("Enter the target URL (e.g., http://example.com): ")
    check_for_datatables(target_url)
