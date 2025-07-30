import subprocess
import re
import sys
#FurkanKAYAPINAR
#CVE-2025-40766

def check_ecs_support(dns_ip):
    try:
        result = subprocess.run(
            ["dig", f"google.com", f"@{dns_ip}", "+subnet=0.0.0.0/0"],
            capture_output=True, text=True, timeout=5
        )
        output = result.stdout

        if "CLIENT-SUBNET" in output:
            print(f"[+] {dns_ip} supports ECS (CLIENT-SUBNET found).")
        else:
            print(f"[-] {dns_ip} does NOT support ECS (CLIENT-SUBNET not found).")

    except subprocess.TimeoutExpired:
        print(f"[!] Timeout while querying {dns_ip}")
    except Exception as e:
        print(f"[!] Error querying {dns_ip}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ecs_dig_check.py <dns_ip>")
    else:
        check_ecs_support(sys.argv[1])
