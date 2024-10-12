# CVE-2024-42849
An issue in Silverpeas v.6.4.2 and lower allows a remote attacker to cause a denial of service via the password change function.

## Writeup
If the password change request is intercepted and a sufficiently long(1MB) string is supplied as the password to use, system resources will be overwhelmed by the attempt to hash the password and cause a DoS.

## Proof of Concept(PoC)/Steps to Reproduce
1. Generate a 1MB long string.

![Generate a long string](https://github.com/njmbb8/CVE-2024-42849/blob/main/command.PNG?raw=true)

2. Intercept request using Burpsuite or similar, send it to Intruder and set the new and confirmation passwords as payload positions.

![Sending request to intruder](https://github.com/njmbb8/CVE-2024-42849/blob/main/send2intruder.PNG?raw=true)

3. Load the file generated in step 1 as a payload.

![Setting the payload](https://github.com/njmbb8/CVE-2024-42849/blob/main/intruder1.PNG?raw=true)

4. Once the attack is started, resource usage should skyrocket and the Silverpeas application will become unresponsive.

![High resource usage](https://github.com/njmbb8/CVE-2024-42849/blob/main/usage.PNG?raw=true)
