# ZeroDayX PoC for CVE-2025-26909

<img width="983" alt="Screenshot 2025-03-28 063552" src="https://github.com/user-attachments/assets/979fb5e5-7e74-48de-a883-fc96856b0fe9" />


This script is a proof of concept (PoC) for detecting vulnerabilities in WordPress plugins, specifically targeting the "Hide My WP" plugin. It checks for the presence of a known vulnerability (CVE-2025-26909) that allows unauthenticated local file inclusion.

## Features

- Checks multiple target URLs concurrently using threading.
- Displays results in color-coded format:
  - Green for vulnerabilities found.
  - Yellow for no vulnerabilities found.
  - Red for unreachable targets.
- Allows the user to specify the number of threads for requests (1 to 8).

## Requirements

To run this script, you need to have Python 3.x installed on your machine. Additionally, you will need the following Python packages:

- `requests`
- `colorama`

You can install the required packages using pip:

```bash
pip install requests colorama
