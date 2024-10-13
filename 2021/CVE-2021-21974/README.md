# ESXi_ransomware_scanner
A program that scans IP addresses for signs of ESXi compromise by grabbing the ransom note from an html page and comparing the strings.

## Requirements
- python 3.x
- requests
- BeautifulSoup
- tqdm
- colorama

## Installation
Use the package manager pip to install the required packages.

```python
    pip install requests
    pip install bs4
    pip install tqdm
    pip install colorama
```
## Usage
Run the program with Python 3:

```python
python ESXi_EZ_Scanner.py
```
## Menu
The program will display the following menu:

## Scanning a single IP address
Select option 1 from the menu and enter the IP address you wish to scan. The program will then display a message indicating whether the IP address is infected or not.

## Scanning IP addresses from a CSV file
Select option 2 from the menu and enter the name of the CSV file. The file should contain a list of IP addresses, with one IP address per row. The program will then scan each IP address and display a message indicating whether each IP address is infected or not.

## Scanning IP addresses from a JSON file
Select option 3 from the menu and enter the name of the JSON file. The file should contain a list of IP addresses, with each IP address represented as a string in the list. The program will then scan each IP address and display a message indicating whether each IP address is infected or not.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
