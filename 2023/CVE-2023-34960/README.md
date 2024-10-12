## 🧱 **ChExp DDoS**

Automatic vuln scanner and exploiter for l7 ddos attacks using Chamilio CVE-2023-34960.

## 🦠 **Zombies system**

The script is automatically scanning and exploiting vulnerables websites from a list for you. Infected websites are saved to results.txt and can be used in your futures attacks.

## 🔎 **How to use**

 1. Install the requirements with `sudo apt-get install python3 python3-pip git wget screen`
 2. Git clone the repository and extract it with `git clone https://github.com/dvtarsoul/ChExp && cd ChExp`
 3. Type `pip/pip3 install threadpool requests`
 4. Now type `python3 chamilio.py`
 5. Type `python3 chamilio.py -f url.txt -t https://yourtarget.com attack_time` and replace https://yourtarget.com and attack_time

## 📝 **Commands**

```bash
usage: ch.py [-h] [-u URL] [-f FILE] [-c CMD] [-t TARGET] [duration]

positional arguments:
  duration              Duration for DDoS in seconds

options:
  -h, --help                   show this help message and exit
  -u URL, --url URL            Target URL; Example: python3 chamilio.py -u http://...
  -f FILE, --file FILE         url_list; Example: python3 chamilio.py -f url.txt
  -c CMD, --cmd CMD            command; Example: python3 chamilil.py -c http://...
  -t TARGET, --target TARGET   Target URL for DDoS; Example: python3 chamilio.py -t http://... DURATION (in seconds)
```

## 🚀 **Methods**

Currently the DDoS method used on the vulnerables wensites is some GET requests. 
There is absolutely no bypass and this script can only down small unsecure sites.

## 💿 **Credits**
 - tarsoul
 - Chamilio CVE-2023-34960

## ⚠️ Disclaimer

```
All tools and projects are created for educational purposes and ethical hacking. Please use responsibly. I'm not responsible of your acts.
```
