## EternalBlue = MS17-010 vulnerability


The code is a script written in Ruby that is part of the Metasploit Framework. Metasploit is a tool used by security professionals to test the security of computer systems and networks. It helps identify vulnerabilities and provides a platform for developing and executing exploits.

The script is used to detect the MS17-010 vulnerability, also known as EternalBlue. This vulnerability affected Windows systems and gained significant attention due to its role in the WannaCry ransomware attack.

The script attempts to determine if a target system is vulnerable to MS17-010 by performing a specific type of communication with the target system using the SMB protocol, which is used for file sharing and communication in Windows networks. By analyzing the response received during this communication, the script can determine if the target system is vulnerable to MS17-010 or not.

The script uses various functions and APIs provided by the Metasploit Framework to construct and send the necessary packets to the target system, and then interprets the response to make an assessment.
