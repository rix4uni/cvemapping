# CVE-2022-0482 Vulnerability Exploitation

# Introduction
This document outlines the detailed analysis of CVE-2022-0482, a critical security vulnerability identified in the Easy!Appointments scheduling software. This flaw, related to Incorrect Authorization under CWE-863, allows unauthorized access to personally identifiable information without proper authentication, posing significant risks to data confidentiality and integrity.

### Author
Mija Pilkaite

# Vulnerability Overview
CVE-2022-0482 impacts versions of Easy!Appointments prior to 1.4.3. It was first reported by Francesco Carlucci on January 30th, 2022. The vulnerability enables unauthorized users to access and potentially exploit sensitive data managed by the software.

# Environment Setup
To analyze this vulnerability, an isolated environment was created using the following steps:

### Preparing the Virtual Environment:
Utilize Ubuntu 22.04 Server within a virtual machine or Docker container.
Download the vulnerable version (1.4.2 or earlier) of Easy!Appointments from the official [GitHub repository](https://github.com/alextselegidis/easyappointments) 
### Configuration:
Modify the PHP version to 8.0 in docker/server/Dockerfile.
Configure config.php as per the documentation.

Installation Commands:
```
docker compose up -d
docker exec -it <container_name> bash
apt install git
apt install npm
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
```
Dependency Installation:
```
npm install
php composer.phar install
```
# Exploitation Process
The exploitation involves the following steps:

### Accessing the Software:
Launch the application and set up an admin profile by logging in at http://localhost/index.php/backend.
### Exploiting the Flaw:
The vulnerability exists due to the absence of adequate security checks on the endpoint /index.php/backend_api/ajax_get_calendar_events.
An attacker can exploit this by making POST requests with "startDate", "endDate", and "csrfToken" to retrieve appointment details in JSON format.
### Obtaining Sensitive Information:
Comprehensive details of all clients, appointment specifics, and service provider information including hashed passwords can be exposed.
### Example of Exploit Command:
`cve-2022-0482.py [-h] [--startDate STARTDATE] [--endDate ENDDATE] hostname`

# Mitigation and Recommendations
Patch Upgrade: It is crucial to upgrade to version 1.4.3 or later, which addresses this vulnerability.
Security Best Practices: Implement strong authentication and authorization checks, especially for sensitive endpoints.

## Bibliography

- **National Vulnerability Database - CVE-2022-0482**: [NVD Detail](https://nvd.nist.gov/vuln/detail/CVE-2022-0482)
- **huntr by ProtectAI**: [Bounty Details](https://huntr.com/bounties/2fe771ef-b615-45ef-9b4d625978042e26/)
- **DockerHub - Easy!Appointments**: [DockerHub Repository](https://hub.docker.com/r/vanhack/easyappointments)
- **GitHub - Easy!Appointments**: [GitHub Repository](https://github.com/alextselegidis/easyappointments)

These sources provide additional information and technical details about the CVE-2022-0482 vulnerability and are crucial for a deeper understanding and further research into the issue.
