# Update 1-22-2020
There is now a tool from FireEye that will help scan these items below. The key to this is that you need to have enough logs to go back to 1-9-2020 to have a chance to see what was done beyond the exploit was ran.  If it finds .XML payload files then you need to use the information below to make a decision on what action to take.
https://www.fireeye.com/blog/products-and-services/2020/01/fireeye-and-citrix-tool-scans-for-iocs-related-to-vulnerability.html

## Tool Download
https://github.com/citrix/ioc-scanner-CVE-2019-19781
https://github.com/fireeye/ioc-scanner-CVE-2019-19781/

# Detecting Exploitation #

There is not an easy way right now to prove what someone has done. With 4x public exploits they each leave a different artifact\signature which is helpful for detection but is not 100%. The key to remember these are the Public exploits the were private until the 10th and that also doesn’t mean there still are others out there in the wild that people not sharing for their own gains. Exploits are editable in most cases where someone can change the name of the file that will be dropped, the name of the user account, the name of the process, the path of the query and many other options which means the possibilities increase exponentially that someone may have exploited the system. There are also advanced attackers and basic attackers too, one will clean up after themselves and come up with very clever ways to disappear into the system to hide from detection.

If you run Nessus, then you can use this .YAR file below to do a privileged scan to look for the common detection methods.
https://github.com/Neo23x0/signature-base/blob/master/yara/exploit_shitrix.yar 

## Exploit Auditing ##

Great Links about this Auditing Process.
https://nerdscaler.com/2020/01/13/citrix-adc-cve-2019-19781-exploited-what-now/amp/
http://deyda.net/index.php/en/2020/01/15/checklist-for-citrix-adc-cve-2019-19781/ 

Disclaimer just like stated before this will not detect every exploit, but it may help detect some anomalies if the attacker didn’t modify the public exploits and/or didn’t clean up after themselves. Most attackers will use the default exploit, and these are some of the documented artifacts that could be left behind. This list of commands was grabbed from many sources and will be very dynamic as other variants, workarounds and new developments come up. We can count on this changing constantly as more infections happen and further forensics is completed with a larger sample set.

Look at this first for things you didn’t do. If you don’t normally do a lot on your ADC these should be very quiet along with, they may have entries from weeks, months or years ago the last time you were on. There are more precise queries just below. Also understand this is a cat and mouse game even in this blog. As we disclose what we have seen and how to spot how to find the attackers they are using this information against us by changing their tactics to avoid detection.

## Exploitation Check Quick Punch List v1 ##
- 1. Check your License, I have heard of some who rebooted their devices and actually had an expired license.
- 2. Get a Support File aka a Backup System -> Diagnostics -> Get Support File and save that file off.
- 3. All the commands below are in NSCLI and if you SSH into the box and use Shell then you can drop the Shell prefix.
- 4. Check the date on the box to help correlate log findings
  - a. shell date
- 5. Check your config change date
  - a. Shell ls -l /netscaler/ | grep netscaler
  - b. Shell ls -l /nsconfig | grep netscaler
    - i. What is the date of your netscaler.conf? 
    - ii. Does that look right? Look for file links to other places.
- 6. Check local account password file
  - a. Shell ls -lh /etc/passwd
    - i.	Check to see when the file was modified. If after the exploit and it wasn’t you, then you need to change that password as soon as possible.
    - ii. I recommend changing the password to nsroot or any local accounts if any exploits are detected.  In many cases
  - b. Shell cat /etc/passwd
    - i. Look to see what accounts are in there.
    - ii. Root, nsroot, daemon, operator, bin, nobody, sshd, nsmonitor are default.
- 7. Check your Logs
  - a. shell ls -lh /var/logfile
    - i. Are the files there? Are they really small?
    - ii. https://support.citrix.com/article/CTX121898
- 8. Bad File Check
  - a. If any of these files are more or less than 8-9 characters and a random filename, then this is a sign of a more advanced attacker that changed the stock exploit.  If you see this, you need to adjust your remediation accordingly. Pwnpzi1337.xml is the file name for the Project India exploit
  - b. shell ls /netscaler/portal/templates/*.xml
    - i. Should be no XML files here.
    - ii. If infected look at the file dates here.
    - iii.shell ls -lh /netscaler/portal/templates/
  - c. shell ls /var/tmp/netscaler/portal/templates
    - i. This directory should not exist.
    - ii. If infected look at the file dates here.
    - iii.shell ls -lh /var/tmp/netscaler/portal/templates
  - d. shell ls /var/vpn/bookmark/*.xml
    - i. Most commonly doesn’t exist but shouldn’t have XML files in there either.
    - ii. If infected look at the file dates here.
    - iii.shell ls -lh /var/vpn/bookmark/
  - e. shell ls /tmp/.init
    - i. This directory should not exist.
- 9. Cron Jobs (Persistency Methods)
  - a. shell cat /etc/crontab
  - b. shell crontab -l -u nobody
- 10. Crypto Check 
  - a. shell top -n 10
    - i. NSPPE-xx (Packet Engine) should be 100% or close, if another process is there you may have been mined
- 11. PCAP
  - a. Shell find / -name “*.cap”
  - b. Help find any stray capture files that may have been taken.
  - c. This will be a sign of a more advanced attacker that may have been sniffing.
- 12. Shell Logs
  - a. shell cat /var/log/bash.log | grep nobody
    - i. looking for user access from the nobody user.
  - b. shell gzcat /var/log/bash.*.gz | grep nobody
    - i. looking for user access from the nobody user in zipped logs.
- 13.	Apache Log Check
  - a. shell "cat /var/log/httperror.log | grep -B2 -A5 Traceback"
  - b. shell "gzcat /var/log/httperror.log.*.gz | grep -B2 -A5 Traceback”
  - c. shell grep -iE 'POST.*\.pl HTTP/1\.1\" 200 ' /var/log/httpaccess.log -A 1
  - d. shell grep -iE 'POST.*\.pl HTTP/1\.1\" 200 143' /var/log/httpaccess.log -A 1
  - e. shell grep -iE 'GET.*\.xml HTTP/1\.1\" 200' /var/log/httpaccess.log -B 1
  - f. shell grep -i '.pl HTTP/1.1" 200 143' /var/log/httpaccess.log | grep POST
    - i. All these are looking for specific items when it comes to moving .pl and .xml files in or out of the system.
  - g. shell cat /var/log/httperror.log
    - i. This is looking at the raw contents of the file overall this is just to look for other items that stand out.
- 14. Persistent Scripts
  - a. shell ps -aux | grep python
  - b. shell ps -aux | grep perl
  - c. shell ps -auxd | grep nobody
    - i. These are both known persistency methods to use scripts to run reverse shells and other tasks. You should only see the grep command in this list of processes.
    - ii.This goes over some of the findings of another persistency method. This exploit used a malicious process ran by the Nobody user.  https://soolidsnake.github.io/2020/01/17/citrix_malware.html
- 15. Password\Account Check
  - a. shell ls -l /etc/passwd
    - i. Look at the file date too if something has been recently added.
  - b. shell cat /etc/passwd
    - i. Anything look suspicious, local accounts?  
- 16. Check TCP Connections 
  - a. Shell netstat -natu 
  - b. Look for non-local IP addresses in your VLANs. Internal IP should be checked also incase another box was compromised.
- 17. Check your Authentication Profiles
  - a. Were they set to TLS or SSL and now they are PlainText?
    - i. I have seen some get changed in some audits and online.
    - ii. This is also the sign of an advanced attacker too.
  - b. This will relate back to if your configuration ns.conf was changed or not changed luckily.
  - c. If it was PlainText before then you need to work on getting this set to TLS and SSL as soon as possible if you find signs of exploits or not.
- 18. Check your Certificates
  - a. These are the SSL Certificates you may want to rekey especially if your box has been exploited.  
  - b. I recommend if you have any signs of exploitation to rekey your SSL certificates.  Some larger deployments may have a more difficult road ahead because the number of other places that Certificate is bound and the possible outages\disruptions an SSL certificate change may have.
  - c. I have seen some clients not rekey because they had good logs to be able to prove they didn’t do anything beyond doing the exploit and didn’t pivot into the system configuration.  Most clients may only have a couple days of 
- 19. Check your Configuration File for Potential Tier 1 Targets
  - a. View your ns.conf and that will create your Tier 1 Target list which was most likely accessed first if the device was exploited.

## If Exploited ##
Your mileage will always vary on what you need to do based on your threat landscape. Here are some of my thoughts I have been telling customers that have found evidence of an exploit executed. 

What compliance bodies cover your business? Finance\Banking, SOX, PCI, HIPPA, State/Local and Government Laws.

If you are under one of these frameworks, then you need to follow those procedures for those compliance bodies. There are also ethical considerations based on what certifications and professional groups you are part of that have provisions for incident response and disclosure.

Here are links to these two well know Incident Response processes guides
https://security.berkeley.edu/incident-response-planning-guideline 
https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final 

One thing we know so far is that around the 1-10-20 the first public exploit was released and there are some reports of infections on the 9th as that is right when it came out. In most cases the risk is much lower if you patched your system before 2020 versus later this month. 

### CVE-2019-19781 Estimated Risk Threat Ramp ###
December 17th-December 31st Lowest Risk of Exploitation	
January 1-8th Lower Risk of Exploitation	
January 9th-13th – Higher Risk of Exploitation	
January 14th- Present – Highest Risk of Exploitation	

This should come into your process for your next steps.

I have found traces of an exploitation what now?
This still depends, one thing most Citrix ADC deployments don’t get configured is good SNMP and SYSLOG logging and they may not have a good way to search, filter or alert if there are artifacts found. If you have absolute logging and you are confident, they didn’t do anything then you may be able to move on with your life. Then if you did find something and you were able to confidently remove their remote access then you could move on.

But most will find they will find some trails and they may not be able to connect the dots on what was done and where they may have gone to and it could be easier after detection to just reset the devices.

My Next Advice will be changing over the next 2 weeks.

## Sample Incident Response Paths ##

There is no right and perfect answer I can give that will fit everyone’s situation these are my thoughts as of now on 1-19-20 and they may change after this as I learn more about next steps and as things are released on the defense and or attack side related to this vulnerability. There is no right answer, IT security is the land like most lands that is ruled by “it depends”. I highly suggest if you find anything else other than these files only in those 3 directories, I would consider the box compromised and go down the more cautious path.  In some of these I’m suggesting taking the more cautious path especially when there is no logging to confirm what they did or didn’t do.  You need to work with your team to decide the best course of action based on your situation because this is a team sport.  There can always be a better way to fix things like this but based on the evidence you have on the device and around the device (1st Tier Targets) then you may be ok by reducing your risk and going from there. 

- Mitigate: This should be where you start no matter what. With the new firmware or the responder policy.
- Exploits Detected During your Audit.
 		  - Start your incident response process.
- With Good Device Logging
  -	Signs of Advanced Attacks or Persistency
    - Build New and Migrate
  - No Signs of Advanced Attacks or Persistency
    - Remediate and Keep Running
- Without Device Logging
  -	Signs of Advanced Attacks or Persistency
    - Build New and Migrate
    - Factory Reset
  -	No Signs of Advanced Attacks or Persistency
    - Build New and Migrate
    - Factory Reset
- With Good 1st Tier Target Logging
  -	Signs of Advanced Attacks or Persistency
    - Build New and Migrate
    - Factory Reset
  -	No Signs of Advanced Attacks or Persistency
    - Remediate and Keep Running
- No 1st Tier Target Logging
  -	Signs of Advanced Attacks or Persistency
    - Build New and Migrate
    - Factory Reset
  -	No Signs of Advanced Attacks or Persistency
    - Build New and Migrate
    - Factory Reset

## Response Definition and Thoughts ##
- Build New and Migrate – Start your incident response process then you can start this process https://docs.citrix.com/en-us/citrix-hardware-platforms/mpx/migrating-configuration-of-existing-appliance-to-another-appliance.html. This is relatively easy for VPX and SDX customers because of the virtual nature and the flexibility of the configuration platform.  MPX Migrations are a different story because of how the factory reset works and the base image is maintained, there could a very low risk if it was an advanced attacker to persist through a firmware upgrade and or factory reset. The likelihood may be lower, but it is still possible (just like anything in the cyber world). 
- Factory Reset – Start your incident response process and remove the .xml files and anything else detected and reboot and check for persistency again.  Then start the process to do the factory reset. There are scripts that can be obtained from Citrix that will go through the process. This will wipe the system to the lowest level before reloading the operating system, but everyone will trust this method so far based on their threat landscape and may want more.
  - The most drastic method would be to RMA the devices to get the drives reloaded and this may be a good or a bad idea based on your lifecycle, platform and your redundancy plan too. I would only suggest that if you saw advanced techniques used and have confirmed lateral movement based on their techniques to go possibly go down this path. I know Citrix is working on a what if options and
- Remediate – Start Incident response process and remove the .xml files and anything else detected and reboot and check for persistency again.  If you have good logs then you will know if anything was done, if not then I would look at your threat landscape and if you have logging on 1st Tier Targets or anything else to know if you need to consider it needing to be factory reset and/or if you need to build new & Migrate.

## Logging Tiers ##
- Good Local Logging
  - You are in the best position to see what happened locally to know if there were any attempts of lateral movement of if the exploit was just ran like most.
- Good 1st Tier Target Logging
  - You are in the best position to see if lateral movement happened or was even attempted. These should be the first things that may be targeted and if you saw successful lateral movement then you should be the most worried and proceed with more caution on your remediation path. If not, then the then you have can lower the risk of the threat and just take the remediation path.
- No Local Logging
  - You are in the worst position to see what happened locally to know if there were any attempts of lateral movement of if the exploit was just ran like most. You have to proceed with more caution on your remediation path.
- No 1st Tier Target Logging
  - You are in the worst position to see if lateral movement happened or was even attempted. These should be the first things that may be targeted and if you saw successful lateral movement then you should be the most worried and proceed with more caution on your remediation path.

I hope people can remove infection and have good enough logging to feel confident they are no longer in and be able to resume your normal activities without some of these steps.

## Other Good Follow-up Steps ##

There are two main things you need to make a decision on if there are any traces of exploitation.
- 1.	Change NSROOT Password
  - a.	I recommend doing this no matter what you find or what logs you have.  This is a chance to get nsroot in rotation for PW changes. ADC Management should be bound to LDAP and NSROOT should only be used for emergencies.
- 2.	Change LDAP Service Account (or another authentication service)
  - a.	Change this password along with I recommend changing to another account if possible so you will have different SID too.  This can be a passive change without anyone noticing if tested before the rollout.
- 3.	Change SSL Keys
  - a.	Good Logging
    - i.	Maybe you are fine if you are 100% sure it is good. 
    - ii.	There is still a part of me that wants to say rekey all the things, but I know how much work that can be in a large shop.
  - b.	No Logging
    - i.	I think you have to rekey everything on there.  There is PEM and PFX protection, but I have seen a lot of places that use very simple passwords for those and could be brute forced offline.  Since we don’t know we need to protect the company.

### Password Thoughts ###
I recommend changing your passwords for all your local accounts on the box if there is any inkling of a successful exploit. Go ahead and change it because in many deployments it may have never been changed after it was originally deployed 4-7 years ago. If you see signs of command line access and/or tampering you can most likely count on the attacker being able to crack the password on Pre 11.0 firmware’s it was AES256 and in later builds it is using AES512 which can also be susceptible with cracking too. Make sure it is bound to LDAP securely also and you have alerts setup for NSROOT logins.

### LDAP Thoughts ###
If you have saw some levels of exploitation, I would also make sure and change any service account that was defined within the Citrix ADC configuration. The most common is the LDAP\Kerberos bind account. Someone getting an exploit to run on a Citrix ADC doesn’t mean they are Domain Admins, but it may not take too long depending on your controls and logging.  This is a very easy change that if tested can be seamless to users.

### Certificate Thoughts ###
Depending on what you found with your audit will help figure this one out too.  If you had good logging and you can see access requested to this file, then you must rekey. If you don’t have good logging, then you should also rekey. If you have a wildcard certificate, then that is also another big problem too and the more sites it is bound to the more your risk and exposure will be.  The worse thing that can happen is that you assume it is ok and someone is standing up phishing site with your certificate that all your training will not prevent the clicks.  This can lead to much bigger problems if someone has access to your certificates and I would suggest proceeding with caution and doing a rekey.  This could be an ok time based on the expiration date of the current certificate.  I have seen some swap to another certificate registrar in this process to just to change things up, but they had logs that the file was accessed and downloaded along with other advanced techniques were detected.

### Credits ###

Last but not least some credits for some of the people that have been working on this issue since it first arrived. There are so many more people that are not on this list because they behind the scenes that I have not seen too.

- Citrix Team – Working to get the information out there along with working on these new firmware’s. They are having to work on 5 patches at once based on the differences with the code families which makes this that much more difficult.
- Daniel Weppeler @_DanielWe – Logging Responder Policy to Detect Probes\Attacks
- Florian Roth @cyb3rops – Nessus YAR File for Exploitation Detection
- CTP Anton van Pelt @AntonvanPelt & CTA Mads Petersen @mbp_netscaler & Jan Tytgat
@jantytgat – Constant work with the CTP\CTA and Citrix Teams to work on many fronts.
- KevTheHermit @KevTheHermit – AWS Instance Password Vulnerability Disclosure on top of the CVE
- Bad Packets Report @bad_packets – The Whole Bad Packets Team https://badpackets.net
- Kevin Beaumont @GossiTheDog – Tons of promotion of the problems seen along with some details on his honeypot and what he has seen.
- Mpgn @mpgn_x64 – Details on the exploit and variations of the exploits
- Nick Carr @ItsReallyNick – Details on the exploit and incident response tips.
- Digi Cat u/digicat – Reddit User, Amazing Running News Blog.
- Ben Sadeghipour @NahamSec – DFIR YouTube video and other contributions
- SANs Team – Articles and DFIR and Deep Dive Videos
- Craig Dods @0xCraig – Password Implications and Research
- Manuel Kolloff @manuelkolloff – Exploitation Post Exploit walkthroughs.
- FireEye and Mandient Team Team Thank you to Rick Cole for creating our earliest detection coverage and the team of Mandiant incident responders for input for this blog—especially Austin Baker, Brandan Schondorfer and John Prieto—and for all of the consultants who are responding to or securing their client environments from this vulnerability. Thanks also to Nicholas Luedtke from our Vulnerability Intelligence team for his assistance in refining this blog’s disclosure and tooling timeline.

