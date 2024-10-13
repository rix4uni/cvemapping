CVE: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2005-0603
--------------------------------------------------------
[N]eo [S]ecurity [T]eam [NST]® - Advisory #06 - 25/02/05
--------------------------------------------------------
Program:  phpBB 2.0.12
Homepage:  http://www.phpbb.com
Vulnerable Versions: phpBB 2.0.12 & Lower versions
Risk: Low Risk!!
Impact: Full path disclosure

      -==phpBB 2.0.12 Full path disclosure==-
---------------------------------------------------------

- Description
---------------------------------------------------------
phpBB is a high powered, fully scalable, and highly customizable
Open Source bulletin board package. phpBB has a user-friendly
interface, simple and straightforward administration panel, and
helpful FAQ. Based on the powerful PHP server language and your
choice of MySQL, MS-SQL, PostgreSQL or Access/ODBC database servers,
phpBB is the ideal free community solution for all web sites.

- Tested
---------------------------------------------------------
localhost & many forums

- Explotation
---------------------------------------------------------
phpBB/viewtopic.php?p=6&highlight=\[HaCkZaTaN]

It'll come out something like this.

Warning: Compilation failed: missing terminating ] for
character class at offset 20 in /home/nst/forum/viewtopic.php(1110) :
regexp code on line 1

It'll give a full path disclosure and also one thing that i noticed is
that the posts change it doesn't come out nothing.
In the HighLight Variable

Here is the problem:
-----[ Start Vuln Code ] ------------------------------------

1106: if ($highlight_match)
1107: {
1108: // This was shamelessly 'borrowed' from volker at multiartstudio dot de
1109: // via php.net's annotated manual
1110: $message = str_replace('\"', '"', \
substr(preg_replace('#(\>(((?>([^><]+|(?R)))*)\<))#se', "preg_replace('#\b(" . \
$highlight_match . ")\b#i', '<span style=\"color:#" . $theme['fontcolor3'] . \
                "\"><b>\\\\1</b></span>', '\\0')", '>' . $message . '<'), 1, -1)); 1111: }

-----[ Ends Vulns Code ] ------------------------------------
Don't borrow stuff lol.

- Exploit
---------------------------------------------------------
Not Yet xD
 
- Solutions
--------------------------------------------------------
Not Yet xD

OK other thing that i noticed was in php.ini

magic_quotes_gpc = On
magic_quotes_sybase = Off

you have to turn both of them ON

- References
--------------------------------------------------------
http://neossecurity.net/Advisories/Advisory-06.txt


- Credits
-------------------------------------------------
Discovered by HaCkZaTaN <hck_zatan@hotmail.com>

[N]eo [S]ecurity [T]eam [NST]® - http://neossecurity.net/

Got Questions? http://neossecurity.net/

Irc.InfoGroup.cl #neosecurityteam

- Greets
--------------------------------------------------------
           Paisterist
           T0wn3r
	   Heap
           Nitrous
           CrashCool
           eL_mEsIaS
           Makoki

           And my Colombian people
