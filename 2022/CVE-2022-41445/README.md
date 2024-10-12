# CVE-2022-41445
Cross Site Scripting in Teacher's Record Management System using CodeIgnitor

> [Suggested description]
> A cross-site scripting (XSS) vulnerability in Record Management System
> using CodeIgniter 1.0 allows attackers to execute arbitrary web scripts
> or HTML via a crafted payload injected into the Add Subject page.
>
> ------------------------------------------
>
> [Additional Information]
> Proof Of Concept: https://phpgurukul.com/teachers-record-management-system-using-codeigniter/
>
> ------------------------------------------
>
> [Vulnerability Type]
> Cross Site Scripting (XSS)
>
> ------------------------------------------
>
> [Vendor of Product]
> Phpgurukul
>
> ------------------------------------------
>
> [Affected Product Code Base]
> Teachers Record Management System using CodeIgniter - 1.0
>
> ------------------------------------------
>
> [Affected Component]
> Source Code
>
> ------------------------------------------
>
> [Attack Type]
> Remote
>
> ------------------------------------------
>
> [Impact Code execution]
> true
>
> ------------------------------------------
>
> [Attack Vectors]
> to Exploit the Vulnerability Attacker need to Login With Admin Account First and then attacker need to goto Add Subject Page then in Add Subject Page Attacker need to Add the Arbitrary JavaScript Payload then Click Submit once subject added successfully, now Login with Teacher Account and Goto User Details then Profile View, once you will visit the Profile View the Payload will Execute
>
> ------------------------------------------
>
> [Reference]
> https://phpgurukul.com/teachers-record-management-system-using-codeigniter/
> https://drive.google.com/file/d/18OjJQA2-8-Hdt0HTMwp4aL_Mp_WuffvL/view?usp=sharing
>
> ------------------------------------------
>
> [Discoverer]
> RashidKhan Pathan

Use CVE-2022-41445.
