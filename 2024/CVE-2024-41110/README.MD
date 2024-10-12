# CVE-2024-41110 Docker Security Checker

This tool is designed to check multiple hosts for vulnerabilities related to CVE-2024-41110 in Docker installations. It specifically looks for vulnerable Docker versions and the use of AuthZ plugins, which can potentially lead to security issues.

## Features

- Checks multiple hosts in parallel for efficient scanning
- Detects vulnerable Docker versions
- Identifies usage of AuthZ plugins
- Generates a comprehensive summary report
- Provides a remediation plan for affected hosts
- Supports both password-based and key-based SSH authentication

## Requirements

- Python 3.6 or higher
- Fabric library (`pip install fabric`)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/vvpoglazov/cve-2024-41110-checker.git
   cd cve-2024-41110-checker
   ```

2. Install the required Python library:
   ```
   pip install fabric
   ```

## Usage

Run the script with the following command:

```
python cve_2024_41110_checker.py <username> <hosts_file> <output_directory> [-k <key_file>]
```

- `<username>`: SSH username for connecting to the hosts
- `<hosts_file>`: Path to a file containing a list of hostnames or IP addresses (one per line)
- `<output_directory>`: Directory where the script will store individual host reports and the summary report
- `-k <key_file>`: (Optional) Path to SSH private key file for authentication

Examples:

Using password-based authentication:
```
python cve_2024_41110_checker.py admin hosts.txt ./reports
```

Using key-based authentication:
```
python cve_2024_41110_checker.py admin hosts.txt ./reports -k /path/to/private_key
```

If you don't provide the `-k` option, the script will prompt you for the SSH password. Using key-based authentication is recommended for better security, especially in production environments.

## Output

The script generates two types of output:

1. Individual host reports: Detailed information about each host's Docker installation and vulnerability status.
2. Summary report: An overview of all scanned hosts, including:
   - Total number of hosts checked
   - Number of vulnerable hosts
   - Number of hosts without Docker running
   - Number of hosts with errors during the check
   - List of vulnerable hosts with their Docker versions
   - Remediation plan

The summary report is both saved to a file and displayed in the console after the script finishes execution.

## Affected Docker Versions

This tool checks for the following vulnerable Docker versions:

- v19.03.15 and earlier
- v20.10.27 and earlier
- v23.0.14 and earlier
- v24.0.9 and earlier
- v25.0.5 and earlier
- v26.0.2 and earlier
- v26.1.4 and earlier
- v27.0.3 and earlier
- v27.1.0

## Remediation

If vulnerable hosts are detected, consider the following remediation steps:

1. Update to the most recent patched version of Docker.
2. If immediate update is not possible:
   - Avoid using AuthZ plugins
   - Restrict access to the Docker API to trusted parties, following the principle of least privilege

## Disclaimer

This tool is provided as-is, without any warranties. Always test in a controlled environment before using in production.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/vvpoglazov/cve-2024-41110-checker/issues) if you want to contribute.

## Links

[https://nvd.nist.gov/vuln/detail/CVE-2024-41110](https://nvd.nist.gov/vuln/detail/CVE-2024-41110)

## Author

Vladimir Poglazov - [GitHub](https://github.com/vvpoglazov)
