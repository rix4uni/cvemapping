# CVE-2022-46836 - Remote Code Execution
This exploit abuses an authenticated remote code execution CVE in Checkmk <= 2.1.0p10, Checkmk <= 2.0.0p27, and Checkmk <= 1.6.0p29 to create a reverse shell.

* **CVE-2022-46836** - PHP code injection in watolib auth.php and hosttags.php allows us to write arbitrary php code into the application. This injection is possible because the settings provided in the profile of a user are inserted into a php file. The settings are placed between single quotes and any attempts to enter a single quote as input is filtered by the system prepending a backslash. This backslash can be bypassed by prepending our own backslash. The injected PHP code is triggered upon accessing the application. Specifically the NagVis component of the application. This allows the execution of arbitrary commands on the system. 

This exploit can be chained with other vulnerabilities in the system for unauthenticated remote code execution instead. Perhaps this version will be released at a later date. The exploit chain is described in the following article: https://www.sonarsource.com/blog/checkmk-rce-chain-1/

DISCLAIMER: This script is made to audit the security of systems. Only use this script on your own systems or on systems you have written permission to exploit.

