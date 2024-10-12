# RaspAP Hunter

RaspAP Hunter is a Bash script designed to scan for RaspAP installations and test them for a specific vulnerability CVE-2022-39986.

```
    ____                       ___     ____ 
   / __ \ ____ _ _____ ____   /   |   / __ \
  / /_/ // __ `// ___// __ \ / /| |  / /_/ /
 / _, _// /_/ /(__  )/ /_/ // ___ | / ____/ 
/_/ |_| \__,_//____// .___//_/  |_|/_/      
    __  __         /_/   __                    author: mind2hex
   / / / /__  __ ____   / /_ ___   _____    
  / /_/ // / / // __ \ / __// _ \ / ___/    
 / __  // /_/ // / / // /_ /  __// /        
/_/ /_/ \__,_//_/ /_/ \__/ \___//_/         
                                                         c=====e
   ____________                                         _,,_H__
  (__((__((___()    CVE-2022-39986                     //|     |
 (__((__((___()()_____________________________________// |ACME |
(__((__((___()()()------------------------------------/  |_____|

```

## Features
1. **Requirements Checking**: Checks for necessary dependencies and provides instructions for installation if missing.
3. **Shodan Integration**: Downloads and parses target IP addresses with RaspAP from Shodan.
4. **Vulnerability Scanning**: Scans for the specific CVE and provides feedback on vulnerable IPs.
5. **Reverse Shell Spawning**: Allows the user to spawn a reverse shell on a vulnerable target.

## Prerequisites

- shodan
- jq
- python
- ngrok
- terminator

## Usage

1. Clone this repository or download the script `raspap_hunter.sh`.
2. Make the script executable:

    ```bash
    chmod +x raspap_hunter.sh
    ```

3. Run the script:

    ```bash
    ./raspap_hunter.sh
    ```

## Notes

- Ensure that `php-reverse-shell.php` is available in the working directory or it will be downloaded from the provided URL.
- Make sure to configure Shodan with your API key.
- Follow the instructions if missing dependencies.

## Author

mind2hex

## Disclaimer

This script is for educational and research purposes only. Do not use this against any systems without explicit permission.

## License

Please see the license file in the repository.