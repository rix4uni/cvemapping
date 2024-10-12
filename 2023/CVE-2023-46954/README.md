# CVE-2023-46954

> SQL Injection vulnerability in Relativity Server 2022
> v.12.1.537.3 Patch 2 and earlier allows a remote attacker to execute
> arbitrary code via the name parameter.
>
> ------------------------------------------
>
> [Vulnerability Type]
> SQL Injection
>
> ------------------------------------------
>
> [Vendor of Product]
> Relativity ODA LLC
>
> ------------------------------------------
>
> [Affected Product Code Base]
> Relativity Server 2022 v.12.1.537.3 Patch 2 and earlier
>
> ------------------------------------------
>
> [Affected Component]
> POST /Relativity.Rest/API/Relativity.Users/workspace/<id>/users/retrieveusersby
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
> Within the JSON POST parameter 'Name', the following payload will return true and display a list of names and emails:
>
> (SELECT (CASE WHEN (1=1) THEN 03586 ELSE 3*(SELECT 2 UNION ALL SELECT 1) END))
>
> But the following payload will return false and display the message 'SQL Statement Failed':
>
> (SELECT (CASE WHEN (1=2) THEN 03586 ELSE 3*(SELECT 2 UNION ALL SELECT 1) END))
>
> Note: the True/False comparison takes place within the CASE WHEN (<here>) clause.
>
> ------------------------------------------
>
> [Reference]
> https://www.linkedin.com/in/jakedmurphy1/
>
> ------------------------------------------
>
> [Has vendor confirmed or acknowledged the vulnerability?]
> true
>
> ------------------------------------------
>
> [Discoverer]
> Jake Murphy
