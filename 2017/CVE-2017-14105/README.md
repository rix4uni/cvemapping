# Aerohive HiveManager Classic Privilege Escalation Vulnerability

Name              Aerohive HiveManager Classic Privilege Escalation Vulnerability  
Systems Affected  HiveManager Classic 8.0r1 8.1r1  
Severity          Medium 6.6/10  
Impact            CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L/E:H/RC:C  
Vendor            http://www.aerohive.com/  
Advisory          http://www.ush.it/team/ush/hack-aerohive/aerohive-priv-exec.txt  
Authors           Sandro "guly" Zaccarini (guly AT guly DOT org)  
Date              20170901  

## I. BACKGROUND

Aerohive Networks HiveManager Classic Online is a cloud-enabled
enterprise-class management system for Aerohive networking products.
HiveManager Classic Online offers simple policy creation, firmware
upgrades, and centralized monitoring of thousands of Aerohive access
points, switches, and branch routers.

Responsible disclosure with Aerohive: Aerohive has a very reactive
security staff.

Their response to our communication was pretty fast, we received the
first ack within 24hrs and an official statement in 4days.

The latest version of the software at the time of writing can be
obtained from support portal at https://support.aerohive.com/login

## II. DESCRIPTION

The vulnerability allows a local user, even restricted as a Tenant, to
upload a backup archive that contain jsp webshell, therefore to execute
code on underlying system.

The affected component is Backup Archive Handler.

Discovered in HiveManager Classic 8.0r1, replicated in 8.1r1.
Older version may be affected too.

## III. ANALYSIS

The HiveManager Classic backup is a plain .tar.gz file with a very
simple structure.

Once the archive is extracted, you will see two folders:

- HiveManager
- dbxmlfile

"dbxmlfile/" contains the HM/VHM configuration, an interesting file to
work on. Anyway our interest moved to "HiveManager/" as it contains a
directory named "tomcat/webapps" which is the default Tomcat web app.

The full tree is something like:

+ tomcat
 + webapps
   + hm
     + domains
       + MyTenant
         + maps
           - ca.png
           - campus.png
           - map_floorplan.png
           - us.png
           - world.png

If such directory is tampered, tar gzipped and then restored using the
backup/restore functionality, an attacker can gain code execution on the
system.

As Proof of Concept a "webshell.jsp" file has been added at maps/ level,
then we created a new .tar.gz archive and tried to restore it.

No error has been thrown and jsp file was available under the docroot at
URI /hm/domains/MyTenant/maps/

Further analysis pointed out that full path was writable so it's 
possible to upload a jsp shell even outside the Tenant scope.

Code will be executed as tomcat (uid/gid 501) allowing a full compromise
of the web UI and access to other Tenant files and configurations as
well.

## IV. WORKAROUND

As main HM admin, create a group with no "Administration -> HiveManager
Operations -> Restore Database // Back Up Database" and
"Administration -> Administrators" privilege.  
Now switch to every VHM and change group to their users.

## VI. VENDOR RESPONSE

Vendor is moving to a completely new release of the product called
HiveManager-NG, which has a different architecture and is not affected
by this vulnerability. We did not perform any audit on such version of
the product.

## VII. CVE INFORMATION

Mitre assigned the CVE-2017-14105 for this vulnerability.

## VIII. DISCLOSURE TIMELINE

* 20170828 Bug discovered
* 20170829 Vulnerability disclosed to Aerohive
* 20170829 First reply from Aerohive
* 20170901 The vendor reply with a wontfix
* 20170901 Request for CVE to Mitre
* 20170901 Got CVE-2017-14105 from cve-assign
* 20170902 Full disclosure
* 20170914 Published a workaround

## IX. REFERENCES

No references.

## X. CREDIT

Sandro "guly" Zaccarini is credited with the discovery of this vulnerability.

Sandro "guly" Zaccarini  
web site: http://www.ush.it/  
mail: guly AT guly DOT org  

## XI. LEGAL NOTICES

Copyright (c) 2017 Sandro "guly" Zaccaini

Permission is granted for the redistribution of this alert
electronically. It may not be edited in any way without mine express
written consent. If you wish to reprint the whole or any
part of this alert in any other medium other than electronically,
please email me for permission.

Disclaimer: The information in the advisory is believed to be accurate
at the time of publishing based on currently available information. Use
of the information constitutes acceptance for use in an AS IS condition.
There are no warranties with regard to this information. Neither the
author nor the publisher accepts any liability for any direct, indirect,
or consequential loss or damage arising from use of, or reliance on,
this information.
