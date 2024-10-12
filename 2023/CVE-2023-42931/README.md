<div align="center">


 #  🇮🇱  **#BringThemHome #NeverAgainIsNow**   🇮🇱

**We demand the safe return of all citizens who have been taken hostage by the terrorist group Hamas. We will not rest until every hostage is released and returns home safely. You can help bring them back home.
https://stories.bringthemhomenow.net/**
</div>
  
# macOS Privilege Escalation Exploit :computer:

I wrote this PoC based on this article  : https://www.alter-solutions.fr/blog/local-privilege-escalating-my-way-to-root-throught-apple-macos-filesystems

This repository contains an exploit script targeting a critical privilege escalation vulnerability (CVE-2023-42931) affecting macOS versions Monterey, Ventura, and Sonoma. 🚨

## Vulnerability Description :warning:

The vulnerability allows unprivileged users to gain full root control over the system by exploiting the "diskutil" command line utility. This poses a significant security risk to affected macOS systems. :lock:

## Exploit Overview :rocket:

The exploit script leverages the "diskutil" command to mount filesystems with specific options, enabling the attacker to escalate their privileges. It involves creating a setuid shell payload, modifying filesystem permissions, copying the payload to a placeholder file, setting permissions and setuid bit, and executing the payload to gain root access. :boom:

## Usage :hammer_and_wrench:

1. Clone the repository.
2. Execute the exploit script.
3. Follow the on-screen instructions.

## Disclaimer :warning:

This exploit script is provided for educational purposes only. Use it at your own risk. The author takes no responsibility for any misuse or damage caused by this script. :warning:

## Credits :clap:

Special thanks to Yann Gascuel (Alter Solutions) for identifying and detailing the vulnerability. :pray:

## License :page_with_curl:

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. :memo:
