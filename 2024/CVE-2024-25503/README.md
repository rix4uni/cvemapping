# CVE-2024-25503
> **Vulnerability type : Cross Site Scripting (XSS)** <br>
> **Product: Advanced REST Client desktop application** <br>
> **Vulnerable Version: 17.0.9** <br>
> **Vendor of the product(s): https://www.advancedrestclient.com/** <br>

## 1. Description
Cross-Site Scripting (XSS) vulnerability in Advanced REST Client v.17.0.9 allows a remote attacker to execute arbitrary code and obtain sensitive information. 
This can be achieved by exploiting a crafted script within the 'edit details' parameter of the New Project function.
<br><br>

## 2. Attack Vectors
This vulnerability arises when an attacker maliciously stores a 'XSS' script in the project description (Markdown format), shares the project with the victim, and then executes the shared project on the victim's PC using the ARC App.
<br><br>

## 3. Proof-of-Concept (PoC)

#### Step 1) Click on the '+ADD A PROJECT' button on the third tab after running the Advanced REST Client.
![image](https://github.com/EQSTLab/PoC/assets/67315168/36cc1f3c-621a-4cdd-ad02-fecfe699496c)

<br><br>

#### Step 2) Click the 'Open details' tab to view the created project.
![image](https://github.com/EQSTLab/PoC/assets/67315168/d010c90b-1d2d-4a69-a274-439f3447bc3b)

<br><br>

#### Step 3) Click on the 'Edit details' tab in the created New Project.
![image](https://github.com/EQSTLab/PoC/assets/67315168/bd23dd0b-7b06-4d54-bb23-25a416f1f770)

<br><br>

#### Step 4) Attacker writes 'XSS script' and clicks 'SAVE' button.

```html
<!--Used 'XSS script' for information leakage-->
<img src=# onerror="alert(document.location)">

<!--Another 'XSS script' for phishing-->
<img src=# onerror="alert(document.location)">
```
![image](https://github.com/EQSTLab/PoC/assets/67315168/1e49e2bc-7d69-4959-9bbd-54cca267e40f)
<br><br>

#### Step 5) When opening a project, a 'XSS script' may generate an alert(information leakage)
![image](https://github.com/EQSTLab/PoC/assets/67315168/7fe20387-1fcd-404c-899f-a4dc96f49a20)
<br><br>

#### or load an attacker's page(phishing).
![image](https://github.com/EQSTLab/PoC/assets/67315168/f911d1c2-453c-4b67-af02-e5b65f13c213)
<br><br>

#### Step 6) Projects created by attackers can be exported through the 'Export project' function.
![image](https://github.com/EQSTLab/PoC/assets/67315168/96495f98-a20c-402d-96c3-88e810683b72)
<br><br>

#### Step 7) Attacker names the project and clicks the 'EXPORT' button to export the project where the 'XSS script' is stored.
![image](https://github.com/EQSTLab/PoC/assets/67315168/0f04ec0c-2059-4b4e-99cc-592776cc87ef)
<br><br>

#### Step 8) This app also has the ability to import a project.
![image](https://github.com/EQSTLab/PoC/assets/67315168/65ce2b37-b88f-4425-a6b8-c5ace0d633cc)
<br><br>

#### Step 9) Victim selects 'import all versions of ARC data' from the top tab to open the projectreceived from the attacker.
![image](https://github.com/EQSTLab/PoC/assets/67315168/98e88c1b-6261-4a77-be33-707a53e7faca)
<br><br>

#### Step 10) When clicking a 'SELECT FILE' button for victim to open malicious project file containing 'XSS script'.
![image](https://github.com/EQSTLab/PoC/assets/67315168/6d0384f9-8c98-42ef-a6d8-df924d934541)
<br><br>

#### Step 11) After the file selection is completed, click the 'IMPORT DATA' button to importsuccessfully.
![image](https://github.com/EQSTLab/PoC/assets/67315168/776294d6-c90d-4f37-a462-be945c687aec)
<br><br>

#### Step 12) Imported file runs and attacker's 'Stored XSS script' runs on victim's 'Advanced RESTClient (ARC) App'.
![image](https://github.com/EQSTLab/PoC/assets/67315168/5fb3181a-5f3f-4ef2-856d-58d8607314dc)
<br><br>

## 4. Additional Information
* If the victim executes a project that includes malicious payloads shared by the attacker, it is dangerous because the victim cannot immediately notice the payload.
  
* For example, this vulnerability can be used to steal sensitive information or perform malicious behavior by reading a user's browser URL.
  
* You can also perform phishing attacks by redirecting users to other sites. Be careful if an XSS vulnerability is exploited in a phishing attack, which can lead to external exposure of sensitive information.
<br><br>

## 5. Discoverer
* E-mail: irene0seo97@gmail.com
* Github: https://github.com/YOUNGSEO-PARK
