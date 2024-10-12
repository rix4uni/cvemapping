> [Suggested description]
> Sourcecodester Password Storage Application in PHP/OOP and MySQL 1.0
> was discovered to contain multiple cross-site scripting (XSS)
> vulnerabilities via the Name, Username, Description and Site Feature
> parameters.
>
> ------------------------------------------
>
> [Additional Information]
> Proof Of Concept: https://drive.google.com/file/d/1ZmAuKMVzUpL8pt5KXQJk8IyPECoVP9xw/view?usp=sharing
> Vendor Homepage: https://www.sourcecodester.com/php/15726/password-storage-application-phpoop-and-mysql-free-source-code.html
> Software Link: https://www.sourcecodester.com/sites/default/files/download/oretnom23/psa_php.zip
>
> ------------------------------------------
>
> [Vulnerability Type]
> Cross Site Scripting (XSS)
>
> ------------------------------------------
>
> [Vendor of Product]
> Sourcecodester
>
> ------------------------------------------
>
> [Affected Product Code Base]
> Password Storage Application in PHP/OOP and MySQL - 1.0
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
> to Exploit this vulnerability attacker need to first create his account on http://localhost/psa_php/owner_registration.php, then login with created password after login, attacker need to inject arbitrary JavaScript code inside Name, Username, Description and Site field, and then click on save, once attacker clicks on save button the arbitrary JavaScript Payload will Execute
>
> ------------------------------------------
>
> [Reference]
> https://www.sourcecodester.com/php/15726/password-storage-application-phpoop-and-mysql-free-source-code.html
> https://drive.google.com/file/d/1ZmAuKMVzUpL8pt5KXQJk8IyPECoVP9xw/view?usp=sharing
>
> ------------------------------------------
>
> [Discoverer]
> RashidKhan Pathan

Use CVE-2022-43117
