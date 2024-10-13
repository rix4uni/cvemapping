                                   _____                      _ _         
         /\                       / ____|                    (_) |        
        /  \   __ _ _   _  __ _  | (___   ___  ___ _   _ _ __ _| |_ _   _ 
       / /\ \ / _` | | | |/ _` |  \___ \ / _ \/ __| | | | '__| | __| | | |
      / ____ \ (_| | |_| | (_| |  ____) |  __/ (__| |_| | |  | | |_| |_| |
     /_/    \_\__, |\__,_|\__,_| |_____/ \___|\___|\__,_|_|  |_|\__|\__, |
                 | |                                                 __/ |
                 |_|                                                |___/ 

##### Docker images verifier cli-tool (CVE-2018-8115)
To help the community stay safe, we at Aqua created an open source tool
that tests images for whether they are safe of this vulnerability.

This uitlity will connect to the Docker Registry (currently only Docker Hub supported) and check whether an image has a malicous file that can exploit the CVE-2018-8115 vulnerability, known to attack the host as part of a "docker pull" command.

## Usage
```sh
$ python verify.py [-h] [--tag TAG] [--arch ARCH] [--os OS] image
```

## Example
```~$ python verify.py evil/image

                               _____                      _ _
     /\                       / ____|                    (_) |
    /  \   __ _ _   _  __ _  | (___   ___  ___ _   _ _ __ _| |_ _   _
   / /\ \ / _` | | | |/ _` |  \___ \ / _ \/ __| | | | '__| | __| | | |
  / ____ \ (_| | |_| | (_| |  ____) |  __/ (__| |_| | |  | | |_| |_| |
 /_/    \_\__, |\__,_|\__,_| |_____/ \___|\___|\__,_|_|  |_|\__|\__, |
             | |                                                 __/ |
             |_|                                                |___/

Docker images verifier cli-tool (CVE-2018-8115)
To help the community stay safe, we at Aqua created an open source tool
that tests images for whether they are safe of this vulnerability.

Aqua Security
https://www.aquasec.com

[~] Fetching evil/image metadata...
[+] Checking layer bce2fbc256ea
[==================================================] 100%
[+] Checking layer cb1aafb71473
[==================================================] 100%
[+] Checking layer 782ba98a8cac
[==================================================] 100%
Found 5 malicious files
 Layer: 782ba98a8cac, File: ../../../../../../../../fromimage.txt
 Layer: 782ba98a8cac, File: Files\../../../../../../../../Users/All Users/Application Data/Start Menu/Programs/StartUp/evil.bat
 Layer: 782ba98a8cac, File: Files\../../../../../../../../Users/All Users/Application Data/Start Menu/Programs/StartUp/Files\script.bat
 Layer: 782ba98a8cac, File: Files\../../../../../../../Resume.txt
 Layer: 782ba98a8cac, File: Files\../../../../../../../Files\text.txt

=== IMAGE IS NOT SAFE! ===
```

 

https://www.aquasec.com
