> [Suggested description]
> Sourcecodester Event Registration App v1.0 was discovered to contain
> multiple CSV injection vulnerabilities via the First Name, Contact and
> Remarks fields. These vulnerabilities allow attackers to execute
> arbitrary code via a crafted excel file.
>
> ------------------------------------------
>
> [Additional Information]
> Proof of Concept: https://drive.google.com/file/d/17rSb8GLFPQfqnVFI56AYffbVMDg8z75t/view?usp=sharing
> Vendor Homepage: https://www.sourcecodester.com/javascript/15214/event-registration-app-export-csv-javascript-free-source-code.html
> Software Link: https://www.sourcecodester.com/sites/default/files/download/oretnom23/registration.zip
>
> ------------------------------------------
>
> [VulnerabilityType Other]
> CSV Injection
>
> ------------------------------------------
>
> [Vendor of Product]
> Sourcecodester
>
> ------------------------------------------
>
> [Affected Product Code Base]
> Event Registration App with Export to CSV in JavaScript - 1.0
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
> in order to exploit this Vulnerability, the attacker need to insert an Excel Formula into the First Name, Contact, and Remarks fields, then click on Save then Click on Export to CSV and then click on Downloaded CSV in Excel once attacker open the Downloaded CSV File in Excel the Payload will Execute
>
> ------------------------------------------
>
> [Reference]
> https://drive.google.com/file/d/17rSb8GLFPQfqnVFI56AYffbVMDg8z75t/view?usp=sharing
> https://www.sourcecodester.com/javascript/15214/event-registration-app-export-csv-javascript-free-source-code.html
> https://www.sourcecodester.com/sites/default/files/download/oretnom23/registration.zip
>
> ------------------------------------------
>
> [Discoverer]
> RashidKhan Pathan

Use CVE-2022-44830.
