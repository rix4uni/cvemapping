# CVE-2024-39031 : Silverpeas Core Stored XSS in in Mes agendas
## Information
<b>Description:</b> In Mes Agendas, a user can create new events and add them to their calendar. Additionally, users can invite others from the same domain, including administrators, to these events. A standard user can inject an XSS payload into the "Titre" and "Description" fields when creating an event and then add the administrator or any user to the event. When the invited user (victim) views their own profile, the payload will be executed on their side, even if they do not click on the event.

<b>Versions Affected:</b> <= 6.3.5

<b>Version Fixed:</b> 6.3.5

<b>Researcher:</b> Tonee Marqus with Phronesis Security (https://www.phronesissecurity.com/)

<b>Applied Fix:</b> https://github.com/Silverpeas/Silverpeas-Core/pull/1346

<b>Related Links</b>:
- https://security.snyk.io/vuln/SNYK-JAVA-ORGSILVERPEASCORE-7443649
- https://avd.aquasec.com/nvd/2024/cve-2024-39031/
- https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-39031
- https://nvd.nist.gov/vuln/detail/CVE-2024-39031
  
## Proof-of-Concept

### Step 1

login as an any user and create a new event (agenda) in the mes agendas.
Inside the “Titre” and “Description” put the following XSS payloads: 

```<script>alert("XSS-Titre")</script>```

And 

```<script>alert("XSS-Description")</script>```

![image](https://github.com/toneemarqus/CVE-2024-39031/assets/85018947/9585a5b2-9aea-417e-91f5-5f210f955044)

### Step 2
Add another user as a participant, for example, here an administrator was added.
![image](https://github.com/toneemarqus/CVE-2024-39031/assets/85018947/be19e3b7-ad7d-4c80-87b7-313e941ad2b4)
![image](https://github.com/toneemarqus/CVE-2024-39031/assets/85018947/c040277f-4745-4865-bb00-b2d8b1106f61)
Save the event:
![image](https://github.com/toneemarqus/CVE-2024-39031/assets/85018947/ff16e47d-a4e2-4c81-a0c0-d50e2f61a64a)

### Step 3
Login to the administrator account and click on the administrator button in the top left to enter administrator profile, once you click, the XSS alert for “Titre” will pop up.
![image](https://github.com/toneemarqus/CVE-2024-39031/assets/85018947/c5ddcc2a-ccab-4700-941e-ff5cc8ab36b8)
If you click OK, the other XSS payload will also pop up for “description”
![image](https://github.com/toneemarqus/CVE-2024-39031/assets/85018947/27d3de65-3b2b-4fc8-be1f-a286520e59bc)

Additionally, the XSS payload can be triggered in many other places, for example when we click on the event from the calendar:
![image](https://github.com/toneemarqus/CVE-2024-39031/assets/85018947/833a0c7a-92e3-46ee-977a-4fd179965b40)
Or from Mon profile → Mur
![image](https://github.com/toneemarqus/CVE-2024-39031/assets/85018947/9e6e56e5-af32-41e1-9d0d-2c3fddf2a402)
Finally, from Fil d'informations:
![image](https://github.com/toneemarqus/CVE-2024-39031/assets/85018947/87dc13c7-0ac2-4b7f-93ae-bc213530e3eb)
