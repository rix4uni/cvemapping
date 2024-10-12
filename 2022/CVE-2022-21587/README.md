# CVE-2022-21587-POC-
CVE-2022-21587 POC 

```
file exploit.py will overwrite to file .pl (not recommended for use, will affect the system) 
file EBS not overwrite, will create a new shell file
```

install slipit:
      git clone https://github.com/usdAG/slipit
      
      cd slipit

      python3 setup.py sdist

      pip3 install --user dist/*

      export PATH=/home/yourname/.local/bin:$PATH
   

install uuencode:
  sudo apt-get install sharutils

Exploit: python3 http|https://example.com
