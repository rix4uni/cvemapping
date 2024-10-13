# cve-2004-2167


Code to be tested:

Download CentOS 6.4 Opertaing System

Download the Latex2RTf to the Downloads folder from the below link:
    
    https://sourceforge.net/projects/latex2rtf/files/latex2rtf-win/1.9.15/

cd /home/username/Downloads/

tar -xvf latex2rtf-1.9.15.tar.gz

 cd latex2rtf-1.9.15
 
sudo make 

sudo make install

gcc -o exploit exploit.c 

./exploit > shell_code.tex

./latex2rtf shell_code.tex

Steps for patching:
Download the patch from:

https://github.com/uzzzval/cve-2004-2167/blob/master/definitions_patch.c

cp definitions_patch.c /home/username/Downloads/latex2rtf-1.9.15/
mv definitions_patch.c definitions.c
sudo Make
sudo make install
./latex2rtf shell_code.tex
