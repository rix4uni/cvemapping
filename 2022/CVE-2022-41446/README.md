# CVE-2022-41446
Privilege Escalation in Teachers Record Management System using CodeIgnitor


> [Suggested description]
> An access control issue in /Admin/dashboard.php of Record Management
> System using CodeIgniter v1.0 allows attackers to access and modify
> user data.
>
> ------------------------------------------
>
> [Additional Information]
> Proof Of Concept: https://drive.google.com/file/d/1Rre498CWp9pWyW9h5ran8GkW6TA2NztC/view?usp=sharing
>
> ------------------------------------------
>
> [Vulnerability Type]
> Incorrect Access Control
>
> ------------------------------------------
>
> [VulnerabilityType Other]
> Privile
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
> user/Users endpoint in url
>
> ------------------------------------------
>
> [Attack Type]
> Remote
>
> ------------------------------------------
>
> [Impact Escalation of Privileges]
> true
>
> ------------------------------------------
>
> [Impact Information Disclosure]
> true
>
> ------------------------------------------
>
> [Attack Vectors]
> to Exploit the Vulnerability Attacker have to login with User account and attacker need to change user/Users endpoint in to admin/Admin endpoint in url,
> > Eg: http://localhost/trms-ci/user/Users/dashboard Change to localhost/trms-ci/admin/Admin/dashboard
>
> ------------------------------------------
>
> [Reference]
> https://phpgurukul.com/teachers-record-management-system-using-codeigniter/
> https://drive.google.com/file/d/1Rre498CWp9pWyW9h5ran8GkW6TA2NztC/view?usp=sharing
>
> ------------------------------------------
>
> [Discoverer]
> RashidKhan Pathan

Use CVE-2022-41446.

