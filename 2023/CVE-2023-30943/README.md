<div align="center">
    
 #  🇮🇱  **#BringThemHome #NeverAgainIsNow**   🇮🇱

**We demand the safe return of all citizens who have been taken hostage by the terrorist group Hamas. We will not rest until every hostage is released and returns home safely. You can help bring them back home.
https://stories.bringthemhomenow.net/**

# CVE-2023-30943
# Moodle Vulnerabilities Exploits


This repository contains combined exploits for two vulnerabilities in Moodle, a widely used open-source learning management system (LMS). The exploits leverage the vulnerabilities to demonstrate Unauthenticated Arbitrary Folder Creation leading to Stored Cross-Site Scripting (XSS) and Self-XSS leading to Account Takeover. Please note that these exploits are provided for educational purposes and should not be used for malicious intent.

## Exploits Overview

### Unauthenticated Arbitrary Folder Creation leading to Stored XSS

Exploit 1 takes advantage of the Unauthenticated Arbitrary Folder Creation vulnerability in Moodle versions 4.1.x before 4.1.3 and 4.2.x before 4.2.0. It showcases how an attacker can create arbitrary folders on the server, leading to Stored XSS. The exploit demonstrates how an attacker can inject malicious code that will be executed when an administrator visits certain panels.

### Self-XSS leading to Account Takeover

Exploit 2 focuses on the Self-XSS vulnerability in Moodle versions before 4.2.2, 4.1.5, 4.0.10, 3.11.16, and 3.9.23. This exploit illustrates how an attacker can craft a malicious link that, when clicked by a victim, triggers Self-XSS. This can potentially lead to an Account Takeover scenario, allowing the attacker to gain control over the victim's account.

## Usage

1. Set up a Moodle instance with the specified vulnerable versions.
2. Customize the placeholder values in the exploits (e.g., `$rev`, `$filepath`, etc.) to match your environment.
3. Execute the combined exploit script, which simulates both vulnerabilities and demonstrates the exploitation process.

Please remember to use these exploits responsibly and only in controlled environments to understand the security risks involved and improve your knowledge of cybersecurity.

## Disclaimer

These exploits are provided for educational purposes only. The intention is to demonstrate how vulnerabilities can be exploited for educational and security awareness purposes. Please refrain from using these exploits for any malicious activities.
</div>
