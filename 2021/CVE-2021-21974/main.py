import argparse
import csv
import json
import requests
import warnings
from tqdm import tqdm
from bs4 import BeautifulSoup
from colorama import Fore, Style


######################################################################
#                                                                    #
#                           ESXi EZ Scanner                         #
#                                                                    #
######################################################################
#                                                                    #
# Author: [Milo]                                                     #
# Date Created: [07/02/2023]                                         #
# Purpose: [Scans IPs for signs of ESXi compromise by grabbing the   #
#           ransom note from html and comparing the strings          #
#                                                                    #
######################################################################


def search_ip(ip):
    try:
        # visit the IP address in the browser, suppress warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = requests.get("http://" + ip, timeout=1, verify=False)

        # parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # search for the strings you mentioned
        found_first_string = "We hacked your company successfully" in soup.text
        found_second_string = "How to Restore Your Files" in soup.text
        if found_first_string and found_second_string:
            print("IP address", ip, Fore.RED + Style.BRIGHT + "IS INFECTED" + Style.RESET_ALL)
    except requests.exceptions.SSLError as error:
        print("Error visiting IP address", ip, ":", error)
    except Exception as e:
        print("Error occurred while visiting IP address", ip, ":", e)


def show_menu():
    print(Fore.RED + Style.BRIGHT + '''

███████╗░██████╗██╗░░██╗██╗░░░░░░███████╗███████╗
██╔════╝██╔════╝╚██╗██╔╝░░║░░░░░░██╔════╝╚════██║
█████╗░░╚█████╗░░╚███╔╝░██║░░░░░░█████╗░░░░███╔═╝
██╔══╝░░░╚═══██╗░██╔██╗░██║░░░░░░██╔══╝░░██╔══╝░░
███████╗██████╔╝██╔╝╚██╗██║░░░░░░███████╗███████╗
╚══════╝╚═════╝░╚═╝░░╚═╝╚═╝░░░░░░╚══════╝╚══════╝''' + Style.RESET_ALL)
    print("Ransomware Scanner!\n")
    print("Please select an option:")
    print("1. Scan a single IP address")
    print("2. Scan IP addresses from a CSV file")
    print("3. Scan IP addresses from a JSON file")
    print("4. Quit\n")
    choice = input("Enter your choice (1-4): ")
    return choice


# set up the command line argument parser
parser = argparse.ArgumentParser(description="Search IP addresses for specific strings.")
group = parser.add_mutually_exclusive_group(required=False)
group.add_argument("--ip", help="a single IP address to search")
group.add_argument("--csv_file", help="a CSV file containing IP addresses to search")
group.add_argument("--json_file", help="a JSON file containing IP addresses to search")

# show menu and get user's choice
choice = show_menu()

# if a single IP address was chosen, get the IP address and search it
if choice == "1":
    ip = input("Enter an IP address: ")
    search_ip(ip)

if choice == "2":
    file_name = input("Enter the name of the CSV file: ")
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        ips = [row[0] for row in reader]
    for ip in tqdm(ips):
        search_ip(ip)

if choice == "3":
    file_name = input("Enter the name of the JSON file: ")
    with open(file_name, 'r') as file:
        ips = json.load(file)
    for ip in tqdm(ips):
        search_ip(ip)

if choice == "4":
    pass

