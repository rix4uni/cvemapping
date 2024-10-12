#  eScan Management Console 
**Exploit Title :** eScan Management Console - Incorrect Access Control                                                          
**Author :** Jeyabalaji                   
**Affected Versions :** 14.0.1400.2281            
**Tested on :** Windows 11   
**CVE :** [CVE-2024-42919](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-42919)             

### **Description:**
The Escan Management Console implements authentication mechanisms; however, the acteScanAVReport endpoint is accessible without requiring any authentication. 

### **Payload :**
acteScanAVReport (Endpoint)

### **Steps to reproduce :**
1. Open eScan Management Console
2. Give 'acteScanAVReport' Endpoint
3. We can able to access the eScan AV Report

### **Mitigation :**

Update to the latest version
