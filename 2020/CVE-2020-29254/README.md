# CVE-2020-29254
TikiWiki 21.2 allows to edit templates without the use of a CSRF protection. 

==========================

Cross-Side-Request-Forgery (CSRF):

TikiWiki 21.2 allows to edit templates without the use of a CSRF protection. 
This could allow an unauthenticated, remote attacker to conduct a cross-site request forgery (CSRF) attack and perform arbitrary actions on an affected system. The vulnerability is due to insufficient CSRF protections for the web-based management interface of the affected system. An attacker could exploit this vulnerability by persuading a user to follow a maliciously crafted url. A successful exploit could allow the attacker to perform arbitrary actions on an affected system with the privileges of the user. These action include allowing attackers to submit their own code through an authenticated user resulting in e.g. path traversal. If an authenticated user who is able to edit TikiWiki templates visits an malicious website, template code can be edited.

### Can be combined with Path Traversal:
In TikiWiki 21.2, an user can be given the permission to edit .tpl templates. This
feature can be abused to escalate the users privileges by inserting the following piece
of smarty code: „{include file='../db/local.php'}“. The code snippet includes
TikiWikis database configuration file and displays it in the pages source code. Any
other www-data readable file like „/etc/passwd“ can be included as well. The config
file displays TikiWikis database credentials in cleartext.
Recommended solution: Disallow including filetypes other than .tpl


# A response from the Tiki project
https://doc.tiki.org/CVE-2020-29254
