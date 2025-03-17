# CVE-2023-34598 - Gibbon v25.0.0 LFI Exploit

This repository contains a Python script that helps identify and exploit a local file inclusion (LFI) vulnerability (CVE-2023-34598) in **Gibbon v25.0.0**. The script can scan a target website for potential vulnerability and, if successful, download the SQL dump for further analysis. It also provides a built-in FOFA query to help locate potentially vulnerable targets.

## Overview

- **Name:** `gibbon_lfi_exploit.py` (example)
- **Purpose:** Identify and exploit a Local File Inclusion (LFI) vulnerability in Gibbon v25.0.0.
- **Primary Features:**
  - **Scan a single target** for vulnerability.
  - **Extract partial database dumps** if the target is vulnerable.
  - **Optionally display** a FOFA query to find more targets.

> **Warning**: This script is intended for educational purposes and authorized penetration testing. Unauthorized use against websites or servers may be illegal and is strictly discouraged. Always obtain proper permission before testing.

---

## Requirements

- **Python 3.x** (Recommended 3.6+)
- **Requests library** (`pip install requests`)

---

## Setup & Installation

1. **Clone** or **download** this repository.
2. Ensure that you have Python 3 installed.
3. Install the required Python libraries:
   ```bash
   pip install requests
   ```
---

## Usage

### 1. Display Help

Run the script without arguments or use the `-h`/`--help` option:

```bash
python3 CVE-2023-34598.py -h
```

This will display an overview of all available commands and options.

### 2. FOFA Query

To display the FOFA query that helps locate potentially vulnerable targets, use:

```bash
python3 CVE-2023-34598.py fofa
```

Copy the displayed query and use it in FOFA to find target URLs.

### 3. Scanning a Single Target

To scan a specific target URL, run:

```bash
python3 CVE-2023-34598.py scan https://example.com/gibbon
```

Replace `https://example.com/gibbon` with the base URL of your Gibbon installation.  
The script will:

1. **Check** the target for vulnerability by requesting `?q=gibbon.sql`.
2. **Identify** if the page contains a specific marker (`"SQL Dump"`).
3. **Create** a new output directory (`Gibbon_dump`, or `Gibbon_dump-2` if the directory already exists, etc.).
4. **Save** the partial SQL dump (if found) into a file named `gibbon.sql` inside the newly created directory.

---

## Script Behavior

1. **Directory Creation**  
   - A directory named `Gibbon_dump` is created if the target is found vulnerable, and the script stores results there.
   - If `Gibbon_dump` already exists, the script creates a new directory named `Gibbon_dump-2`, `Gibbon_dump-3`, etc.

2. **File Outputs**  
   - **`!target.txt`**: Contains the scanned target’s base URL.
   - **`gibbon.sql`**: Contains the extracted SQL dump if markers are found.

3. **Error Handling**  
   - If any network or unexpected error occurs, the script will display an error message and exit.

---

## Example Workflows

### Basic Scan & Dump

1. **Scan & Dump**:
   ```bash
   python3 CVE-2023-34598.py scan https://victim.com/gibbon
   ```
2. If vulnerable, the script creates a folder (e.g., `Gibbon_dump`) and saves `!target.txt` and `gibbon.sql`.

### FOFA Query

1. **Display FOFA**:
   ```bash
   python3 CVE-2023-34598.py fofa
   ```
2. Copy and paste the returned query into FOFA to find a list of targets.

---

## Notes & Disclaimers

- **Legal Usage**: Use this script only on systems you own or have explicit permission to test.  
- **Disclaimer**: The authors assume **no responsibility** for misuse or damage caused by this tool.  
- **For Education Only**: This script is intended to demonstrate exploitation techniques for educational and research purposes.

---

## Credit

Credit to [ @komodoooo](https://gist.github.com/komodoooo/bf9bfea7f229d503e91d108940cf5ec0), this is just a python fork of his ruby repository.
