## TeamCity CVE-2023-42793 Exploit

This Python script exploits a security vulnerability (CVE-2023-42793) in JetBrains TeamCity, allowing an attacker to  create a new user with administrative privileges.

### Usage
The script takes either a single TeamCity instance URL or a list of URLs as input. The provided URL(s) should point to the TeamCity server(s) that are vulnerable to CVE-2023-42793.

#### Single URL:
```bash
python exploit.py -u http://teamcity.example.com
```

#### List of URLs:
```bash
python exploit.py -l url_list.txt
```
![image](https://github.com/H454NSec/CVE-2023-42793/assets/127287794/34239694-f418-46da-8168-9f01234d3be3)

### Dork:
- Google: `intitle:"log in to teamcity"`
- Shodan: `http.component:"TeamCity"`
- Shodan: `http.title:"Log in to TeamCity -- TeamCity"`
- Shodan: `http.title:TeamCity`

### How it Works
1. **Token Deletion**: The script initiates a DELETE request to remove the user token associated with the default user (id:1).
2. **Token Creation**: Upon successful token deletion, a new user token is created for the same default user.
3. **User Creation**: Using the newly generated token, the script then creates a new user with administrative privileges.
4. **Output**: Successful exploits are reported, and the compromised URLs are appended to a file named `vulnerable.txt`.

### Prerequisites
- Python 3.x


## Buy Me a Coffee

Hey Hackers, if this repository has helped you secure the internet, how about buying me a coffee to keep the coding fuel flowing?

[![☕ Buy Me a Coffee!](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/H454NSec)

## 🪙 Cryptocurrency Donations

Feel like going beyond coffee? You can also support this project with cryptocurrency donations:

- **Monero (XMR):** `88m2c6n4rRtE7esrXmSba5K34QX5Rv6BgLCpEH7QtDw9UnW6h82itbGbomvgZFYa6AcwRJ5qzMpf1LMCKGyFbzhTAbJZ7Ew`
- **Bitcoin (BTC):** `bc1qpww8uxflvrjxkm4u3390kf4xtyl7udupw3rrxc`
- **Ethereum (ETH):** `0x1312c0cf549b504a8c5a73f73712f839eb193edc`
### Your support keeps the project alive and motivates me to create more awesome stuff. Cheers! 🚀
## License

This repository is licensed under the [GNU General Public License v3.0](LICENSE).

## Disclaimer
This repository and its contents, including scripts, PoCs, and exploits, are provided for educational purposes only. Usage of these materials should be conducted responsibly and solely on systems for which you have explicit permission to test. Users are required to comply with local laws and adhere to ethical guidelines when utilizing any tools or code from this repository. The author disclaims responsibility for any misuse or damage resulting from the use of the contents within this repository.

# Stars
[![Stars](https://starchart.cc/H454NSec/CVE-2023-42793.svg)](https://starchart.cc/H454NSec/CVE-2023-42793)
