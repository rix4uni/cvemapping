# Confluence_CVE-2021-26084
Remote Code Execution on Confluence Servers : CVE-2021-26084

### PoC

![image](https://user-images.githubusercontent.com/79006904/131671801-7cdd2536-f5e7-4cf9-9106-0d34947265fe.png)


#### Confluence Possible exploit endpoints
``` https://<REDACTED>/users/user-dark-features
https://<REDACTED>/login
https://<REDACTED>/pages/templates2/viewpagetemplate.action
https://<REDACTED>/template/custom/content-editor
https://<REDACTED>/templates/editor-preload-container
https://<REDACTED>/pages/createpage-entervariables.action 
```
### [Credit & Full writeup](https://github.com/httpvoid/writeups/blob/main/Confluence-RCE.md)

### Video : [Video](https://youtu.be/RXLdWwAMjz8)

##### Note : I have tested on version 7.12.4.

### [Thank you alt3kx](https://github.com/alt3kx/CVE-2021-26084_PoC)

# Author
[Vulnmachines](https://www.twitter.com/vulnmachines)

