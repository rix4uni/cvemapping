# CVE-2021-46702
# Description:
Tor Browser 9.0.7 on Windows 10 build 10586 is vulnerable to information disclosure. This could allow local attackers to bypass the intended anonymity feature and obtain information regarding the onion services visited by a local user. This can be accomplished by analyzing RAM memory even several hours after the local user used the product. This occurs because the product doesn't properly free memory.
# Tested Version:
Tor Browser - 9.0.7
# Vendor of Product
https://www.torproject.org/
# Attack Type
Local 
# Impact
Information Disclosure
# Reference 
https://www.sciencedirect.com/science/article/pii/S0167404821001358
# POC Requirements
For the PoC.sh to work, a memory dump of the user work station should be granted. It will provide information about visited sites even after 10 hours from the user interaction.  
You can find the shell script that automate the process of finding the visited onion services in the files section. The following Figure shows the Report file output which indicates the visited sites and additional information:

<img width="826" alt="Screenshot 2022-02-26 at 17 40 35" src="https://user-images.githubusercontent.com/38157380/155847153-38f17ca3-92b2-47fb-bcf3-f7ee47c28d0a.png">


# Discoverer
Malak Alfosail
# Twitter: @malakalfosail
