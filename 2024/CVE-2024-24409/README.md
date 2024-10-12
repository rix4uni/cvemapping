## CVE-2024-24409 - ADManager Plus Build < 7210 Elevation of Privilege Vulnerability
## Description
The Modify Computers is a predefined role in ADManager for managing computers. If a technician user has the Modify Computers privilege over a computer can change the userAccountControl and msDS-AllowedToDelegateTo attributes of the computer object. In this way, the technician user can set Constrained Kerberos Delegation over any computer within the Organizational Unit that the user was delegated.

Contrary to what ADManager claims the user who has the Modify Computers role can change the privilege of computer objects in the Active Directory. The Constrained Kerberos Delegation can be set for any service such as CIFS, LDAP, HOST services. Then the user can access these services by abusing the Constrained Kerberos Delegation. In addition, the Unconstrained Kerberos Delegation can be set over the computer objects by changing the userAccountControl attribute. Normally, only users that have SeEnableDelegationPrivilege privilege can set constrained kerberos delegation. Only members of the BUILTIN\Administrators group have this privilege by default. The delegated user for an Organizational Unit can not set constrained kerberos delegation even if a user has the GenericAll right over a computer account, so the delegation process in Active Directory does not grant this privilege. However, the technician user can use the SeEnableDelegationPrivilege right via the Modify Computers role.

## Vulnerability reasons
ADMP Web App Authorization issue: Assigning a predefined Modify Computers role delegates the technician user to modify custom attributes of computers unexpectedly. Even though it appears that this privilege is not granted in the UI, the Additional Custom Attribute property is assigned and this leads to broken access control vulnerability.

There is no restriction for editing the userAccountControl and msDS-AllowedToDelegateTo attributes of the computer objects. The ADMP application performs changes with domain admin privileges as designed so that if we can bypass some restrictions (e.g. format of attribute value), our requests are applied with domain admin privileges. This way we can edit the attributes userAccountControl and msDS-AllowedToDelegateTo.

## Impact
A technician user elevates privileges from Domain User to Domain Admin. For example, the user can set Constrained Kerberos Delegation over CLIENT1$ for the CIFS service of the domain controller and access the CIFS service. As a result, the user is delegated to manage CLIENT1$ but he can access the CIFS service of the domain controller impersonating a user unexpectedly.

## Proof Of Concept
The attacker user can perform DCSync attack after adding the Constrained Kerberos Delegation for LDAP service with following prerequisites: <br>
`Scenario 1: If the attacker has local admin right over a computer and can manage this computer with the “Modify Computers” role in ADManager Plus` <br>
<br>
`Scenario 2: If the attacker adds a computer to Active Directory (MAQ, delegation) and manage this computer with the “Modify Computers” role` <br>
<br>
`Scenario 3: If the attacker can dump NT hash of a computer account (dumping hash with mimikatz, secretsdump, etc.) and manage this computer with the “Modify Computers” role`

This proof of concept was carried out on ADManager Plus Build 7203.


https://github.com/user-attachments/assets/496b3bfd-a95f-4d69-8ee5-53ae0592ebdb

https://docs.unsafe-inline.com/0day/admanager-plus-build-less-than-7210-elevation-of-privilege-vulnerability-cve-2024-24409
