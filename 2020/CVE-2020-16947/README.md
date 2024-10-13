# CVE-2020-16947
Outlook 2019 Remote Command Execution
This bug occured when parsing html contents. if attacker successfully executes this exploit, it can lead to remote command execution.
When copying strings out of the ascii range among html contents, the corresponding string is replaced with 0xfffd. As a result, the size of the copied string doubles, so despite the same size of the src buffer and dst buffer, buffer overflow occurs.

Please contact Mast3rSpl0it@gmail.com if you are interested in 0Days Exploits.
