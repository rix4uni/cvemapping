# CVE-2009-0229-PoC
PoC for CVE-2009-0229 "Print Spooler Read File Vulnerability" LPE AFR (related to CVE-2020-1048)


## Details
* Author: Andrei Costin (zveriu@gmail.com)
    * https://twitter.com/costinandrei/
* PoC date: 2010-xx-xx
* Release date: 2020-05-14 (reminded/inspired by CVE-2020-1048 - yes, I am too late to the party :D )
* TL;DR
    * If you want 0days, dig Printing and Faxing sub-system of OSes :) - lots of legacy code due to historical reasons - there are vulns for everyone =)

# Notes
* Note1: Unverified - unsure 100% is the same bug that triggers the CVE-2009-0229

* Note2: Unverified - could work on newer systems like Windows Server 2012 and Windows Server 2016

* Note3: All Windows releases come with 4 default "Separator Page" files
    * pcl.sep
    * pscript.sep
    * sysprint.sep
    * sysprtj.sep

* Note4: This trick is older than Windows 95 =), pretty sure it was used by pros for "stealth info recovery" ;)


## Pre-requisites
* (non-admin) local attacker has "printer management rights"
    * option1: can add a new printer
    * option2: can modify settings of an existing "system wide" printer (many times the case)
* "arbitrary file" for exfiltration does not have explicit "Deny Read" permission
    * highly unlikely as that would make accessing files for the victim really unpractical/unusable


## PoC Execution
* Local attacker configures any printer s/he has access to so that it uses "Separator Page" file supplied by the attacker (attack.sep), now attacker has "weaponized printer"
   * See "Windows "Separator Page" References" below for details

* Local attacker crafts the "Separator Page" file (attack.sep) to use the "@F"/"$F" operator, as follows, where the file to be exfiltrated is assumed to be "C:\secret.txt" (notice the \\ and the direct concatenation to @F operator)
```
@
@FC:\\secret.txt
```

* Local attacker needs to print something using the "weaponized" printer above
    * For example, local attacker opens Notepad, prints the empty document through the printer configured above with "Separator Page" file
    * Local attacker uses the "print to file" (e.g., c:\temp\exfiltrated.out) option when printing - there are "print to file" .ps in most Windows versions + .xps in newer ones (http://ps-2.kev009.com/pcpartnerinfo/ctstips/e94a.htm)
        * This is done so that the content of the exfiltrated file does not go to the printer (though this is also an option), but becomes immediately available to the attacker

* Attack improvement: one "Separator Page" file can have a brute-force list of most common filepaths/filenames
* There is also @L operator :)
   * see my "PostScript: Danger Ahead?!" https://scholar.google.fr/scholar?oi=bibs&hl=en&q=related:RGJbW-sFP9sJ:scholar.google.com/
   * see also pscript.sep and sysprint.sep


## Trivia
* Found back in 2010 when I was doing "Hacking Printers for Fun and Profit" research/talks
    * https://www.youtube.com/watch?v=R56ZXErKCeE
    * https://www.youtube.com/watch?v=KrWFOo2RAnk 
    * https://www.youtube.com/watch?v=JcfxvZml6-Y
    * http://andreicostin.com/papers/Conf%20-%20EuSecWest2010_AndreiCostin_HackingPrintersForFunAndProfit_full.pdf
    * found independently from CVE-2009-0229 submitter - until today, I did not know there is this CVE-2009-0229 =)), thought I was sitting on a 0day =))

* I am pretty sure the Printing and Faxing sub-systems are bug-trapped with vulns back since Windows 3.1 (for historical reasons)


## Security References
* "Microsoft Security Bulletin MS09-022 - Critical"
    * https://docs.microsoft.com/en-us/security-updates/securitybulletins/2009/ms09-022
    * https://support.microsoft.com/de-ch/help/961501
* CVE-2009-0229
    * https://nvd.nist.gov/vuln/detail/CVE-2009-0229
    * https://vuldb.com/?id.48511

* CVE-2020-1048
    * https://windows-internals.com/printdemon-cve-2020-1048/

## Windows "Separator Page" References
* This is how "Separator Page" dialogs look on various Windows versions
    * https://www.google.com/search?q=%22Separator+Page%22+windows&source=lnms&tbm=isch
* This is how "Print to file" looks in some Windows versions
    * http://ps-2.kev009.com/pcpartnerinfo/ctstips/e94a.htm
* "Separator Page" in "Hands-On Microsoft Windows Server 2016 By Michael Palmer"
    * https://books.google.fi/books?id=zi-dBAAAQBAJ&pg=PA267&lpg=PA267&dq=%22SYSPRTJ.SEP%22+windows+10&source=bl&ots=TUGyElUQdc&sig=ACfU3U0WMpu6Y3EY5vo5MAJxNE04DjRtbg&hl=en&sa=X&ved=2ahUKEwid6arL6LPpAhUPAxAIHaF9AXYQ6AEwA3oECAcQAQ#v=onepage&q=%22SYSPRTJ.SEP%22%20windows%2010&f=false
* "Create Custom Separator Pages in Windows Server 2012/2016"
    * https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-R2-and-2012/jj149734(v=ws.11)?redirectedfrom=MSDN
* "Use a Separator Page When Printing in Windows"
    * https://computingondemand.com/use-a-separator-page-when-printing-in-windows/
* "How do I configure a Print Separator Page?"
    * https://www.itprotoday.com/cloud-computing/how-do-i-configure-print-separator-page
