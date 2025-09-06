# Form-Tools-3.1.1-RCE
CVE-2024-22722 RCE via SSTI Automation with Python.

Server Side Template Injection (SSTI) vulnerability in Form Tools 3.1.1 allows attackers to run arbitrary commands via the Group Name field under the add forms section of the application. This script automates the creation of a new form and group, and returns with a shell-like interface by modifying the Group Name and returning the executed command results. 
