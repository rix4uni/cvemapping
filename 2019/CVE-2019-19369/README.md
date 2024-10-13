<div align="center">
<h1 style="font-family: 'Source Sans Pro', sans-serif;"><b>CVE-2019-19369 - FusionPBX =< 4.5.10 Authenticated RCE</b></h1>

Authenticated attackers can use PHP-Editor function in FusionPBX versions =< 4.5.10 to edit one of the existing PHP pages to insert a PHP payload. By navigating to the changed file we are able to gain a shell as www-data.
<br>
Discovered by TheCyberGeek

![Adding payload](/p1.png)
![Executing payload](/p2.png)
