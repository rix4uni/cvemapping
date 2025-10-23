# CVE-2025-60852: CSV Injection in Instant Developer Foundation (< 25.0.9600) – Proof of Concept (PoC)

## 📌 Overview

This repository contains a Proof of Concept (PoC) for a **CSV Injection (Formula Injection)** vulnerability (CVE-2025-60852) affecting applications built with the **Instant Developer Foundation** framework (versions prior to 25.0.9600). <span style="color: #0d0d0d;">Applications built with the vulnerable framework do not properly sanitize user-supplied input when exporting data in CSV format.</span>

As a result, spreadsheet software such as **Microsoft Excel** or **LibreOffice Calc** interprets certain values as formulas.

* * *

## Affected Software

- **Framework:** Instant Developer Foundation <span style="color: #0d0d0d;">(framework)</span>
- **Affected Versions:** < 25.0.9600
- <span style="color: #383a42;">**Patch Status**:</span> <span style="color: #383a42;">Fixed in version 25.0.9600.</span>

* * *

## Vulnerability Details

Observed behavior:

- Values starting with **“+”** or **“-”** are directly reflected in the exported CSV file and are interpreted as formulas when opened in spreadsheet software such as Microsoft Excel or LibreOffice Calc.
- Values starting with **“=”** are quoted, suggesting a partial but insufficient mitigation.

### Potential Impacts

- **Local command execution** (via Excel DDE)
- **Data exfiltration** (through HYPERLINK)
- **Data manipulation** in spreadsheets

* * *

## Proof of Concept (PoC)

<span style="color: #383a42;">Insert the following payload in any user-controllable input field.</span>

### Payload

`+CMD|' /C calc'!A0`

<span style="color: #0d0d0d;">When the exported CSV file is opened in Excel with</span> **DDE launch** <span style="color: #0d0d0d;">enabled, the payload triggers execution of</span> `calc.exe` <span style="color: #0d0d0d;">on Windows.</span>

### Steps to Reproduce

1.  Insert the above payload in any **user-controllable input field within a table that can be exported in CSV format** (in an application built with Instant Developer Foundation < 25.0).
    
2.  Export the table as CSV.

![:/images/CSV_Injection_1.png](https://github.com/valeriocassoni/CSV-Injection-in-Instant-Developer-Foundation-25.0-PoC/blob/main/images/CSV_Injection_1.png)
    
3.  Open the exported CSV file in **Microsoft Excel** or **LibreOffice Calc**.
    
4.  If **DDE launch** is enabled in Excel, the system calculator (`calc.exe`) is executed.

![:/images/CSV_Injection_2.png](https://github.com/valeriocassoni/CSV-Injection-in-Instant-Developer-Foundation-25.0-PoC/blob/main/images/CSV_Injection_2.png)

    

🔗 [Excel DDE launch documentation](https://learn.microsoft.com/en-us/office/troubleshoot/excel/security-settings)

## Release notes
🔗 [Release Notes: Instant Developer Foundation - Version 25.0.9600](https://doc.instantdeveloper.com/?ARTID=0A1FE3DB-A827-4122-900D-BD17C7C9F292)

* * *

## Disclaimer

This PoC has been created strictly for **educational and research purposes**.  
Do **not** use this against systems or applications without explicit authorization.  
The author assumes no liability for any misuse of this material.

&nbsp;
