# Connect Box CH7465LG (CVE-2019-13025)

# Information

This repository contains two PoCs for the `Connect Box CH7465LG` running on Firmware `CH7465LG-NCIP-6.12.18.24-5p8-NOSH` or older.

For more information have a look at [my blog](https://xitan.me/posts/connect-box-ch7465lg-rce/).

# Usage

## Unauthenticated Remote Code Execution

> $ python3 poc-rce.py <router_ip> <command>

## Unauthenticated Information Disclosure

> $ python3 poc-information-dump.py <router_ip>

# Credits

xitan 2019.