# Vulnerability Description

File Sharing Wizard 1.5.0 allows a remote attacker to obtain arbitrary code execution by exploiting a Structured Exception Handler (SEH) based buffer overflow in an HTTP POST parameter. 

This exploit was tested on windows 7 Home. It will certainly break when on other platforms. Mainly for research purposes.
