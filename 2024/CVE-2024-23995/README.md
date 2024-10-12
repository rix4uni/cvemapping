# Beekeeper-Studio PoC
A Proof-Of-Concept for CVE-2024-23995 vulnerability.
---------------------------------------

#### 1.Vunerability Overview:
 * Vulnerability Subject: RCE via XSS
 * Vulnerability Version: <= Beekeeper-Studio-4.1.13
 * Attack Type: Remote Code Execution
 * Attack Vectors: To exploit the vulnerability, one must insert malicious scripts into the column names of the table. When hovering the mouse over the corresponding column(tabulator-header-contents), a preview (tabulator-popup-container) should execute, allowing the exploitation to take place.
 * Reserved CVE Number: CVE-2024-23995 
---------------------------------------

#### 2. Vulnerability Cause:
Proof-of-concept (POC)
----------------------

**Step 1) Create a database containing column names written with malicious scripts.**<br><br>
**Step 2) If the attacker is using SQLite, distribute the DB file; for other databases, distribute the connection information for the DB server.**<br><br>
**Step 3) The victim connects to the database, goes into the table, and hovers the mouse over the column names, triggering the execution of the corresponding scripts.**<br><br>
**Step 4) Since there are no restrictions on access permissions for local data, example statements like <img src=# onerror="require(child_process).exec(C:/Windows/System32/calc.exe)"> work successfully.**<br><br>
* While other popup containers are filtered, this specific part lacks proper validation.
---------------------------------------

### 3. Additional Information
![image](https://github.com/EQSTLab/PoC/assets/160688472/5e036402-0a8e-4a8e-98fd-526e2773eba4)
* Use this tabulator-popup-container

![image](https://github.com/EQSTLab/PoC/assets/160688472/e3ca383f-0bc4-4015-8952-92afbbbb3727)
* Create column names written with malicious scripts. like '<img src=# onerror="require(`child_process`).exec(`C:/Windows/System32/calc.exe`)">'

![image](https://github.com/EQSTLab/PoC/assets/160688472/59e96042-d0e4-4369-b2f2-509778254a2b)
* Mouse over the column names, triggering the execution of the corresponding scripts.
