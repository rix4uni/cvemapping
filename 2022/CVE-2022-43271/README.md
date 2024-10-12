# CVE-2022-43271

## Stored Cross-Site Scripting (XSS) 

Product: Move CRM (https://inhabit.com.au/Move-Real-Estate-CRM-Software)

Discovery date: 2/8/2022

Fix date: 4/8/2022

Affected Version: version 4, build 260

Fixed Version: version 4, build 261

Description:
The vulnerability was discovered in the 'staff settings' of the CRM, specifically in the 'Profile' text box. When saving the changes and intercepting the POST request, the 'lProfileCopy' parameter can be modified to include an XSS payload and bypass front-end filtering.
