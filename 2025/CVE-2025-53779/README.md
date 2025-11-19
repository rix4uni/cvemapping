# Invoke-BadSuccessor

Abuse **Delegated Managed Service Accounts (dMSA)** creation rights on vulnerable Organizational Units (OUs) to escalate privileges in Active Directory environments (BadSuccessor vulnerability – CVE-2025-53779).

---

## Overview

`Invoke-BadSuccessor` automates a privilege escalation attack chain by exploiting dMSA misconfigurations and delegation in Windows Server 2025 Active Directory:

- Identifies OUs where the current user (or their groups) has **CreateChild** rights.
- Creates or reuses a **machine account**.
- Creates or reuses a **Delegated Managed Service Account (dMSA)**.
- Grants the user **GenericAll** permissions over the dMSA.
- Configures attributes:
  - `msDS-DelegatedMSAState = 2`
  - `msDS-ManagedAccountPrecededByLink = <DistinguishedName>` (links the dMSA to a privileged account)
- Generates post-exploitation steps ready to use with **Rubeus** (unless `-Quiet` is specified).

This technique abuses dMSA behavior to escalate privileges by forging Kerberos tickets using machine account credentials and requesting TGS tickets for the service account with the privileges of the linked high-privilege account.

---

## Features

- Fully automated dMSA privilege escalation chain.
- Quiet mode (`-Quiet`) suppresses post-exploitation instructions.
- Smart identity resolution for the `-PrecededByIdentity` option (accepts users, computers, or other AD objects).
- Handles common edge cases such as existing accounts, incorrect distinguished names, and missing RID 500 (default admin).
- Purely uses the ActiveDirectory PowerShell module — no external binaries required.

---

## Functions

### Get-ADObjectACL

Low-level ACL enumerator for Active Directory objects. Wraps `Get-Acl` on the `AD:` drive and returns a clean, filterable list of ACEs with:

- `ObjectDN`
- `IdentityReference`
- `SecurityIdentifier`
- `ActiveDirectoryRights`
- `AccessControlType`
- Inheritance flags

Supports:

- `-SearchBase` – limit enumeration to a specific DN (e.g., a target OU)  
- `-ExcludeDefaultSIDs` – filter out noisy built-ins (Everyone, Authenticated Users, SELF, etc.)  
- `-ExcludeAdmins` – filter RID-based domain admin/infra groups (Domain Admins, Enterprise Admins, etc.)

### Find-VulnerableOU

Higher-level enumeration helper using `Get-ADObjectACL` to find OUs where a user (or their groups) has **CreateChild** rights.

It resolves:

- The specified user (or the current user by default)  
- Their transitive group memberships  
- All ACEs where `SecurityIdentifier` is in that token **and** `ActiveDirectoryRights` contains `CreateChild`

### Add-ADObjectACL

Equivalent of PowerView’s `Add-DomainObjectAcl` but only using the ActiveDirectory module. Uses `Get-Acl` / `Set-Acl` on `AD:` to add ACEs.

Supported rights include:

- `All`, `GenericAll`, `GenericRead`, `GenericWrite`
- `CreateChild`, `DeleteChild`
- `ReadProperty`, `WriteProperty`
- `Delete`, `WriteDacl`, `WriteOwner`

### Invoke-BadSuccessor

Main attack chain function that:

1. Finds the first vulnerable OU where the user has **CreateChild**.
2. Creates or reuses a computer account in that OU.
3. Creates or reuses a delegated MSA in that OU.
4. Grants **GenericAll** on the dMSA to the user.
5. Configures:
   - `msDS-DelegatedMSAState = 2`
   - `msDS-ManagedAccountPrecededByLink = <DN>` of a privileged object.
6. Optionally prints Rubeus commands for post-exploitation unless `-Quiet` is set.

---

## Usage

### Basic
```powershell
Invoke-BadSuccessor
```

### Quiet Mode (No Post-Exploitation Tips)
```powershell
Invoke-BadSuccessor -Quiet
```

### Custom Names and DNS
```powershell
Invoke-BadSuccessor -ComputerName "WEB01" -ServiceAccountName "webpool_dMSA" -ServiceDnsHostName "web01.internal"
```

### Custom Predecessor Object
```powershell
Invoke-BadSuccessor -PrecededByIdentity "svc_app"
```

The script automatically resolves this identity in Users, Computers, or domain objects.

---

## Post-Exploitation with Rubeus
Example commands generated for ticket forging:
```
Rubeus.exe hash /password:'Password123!' /user:Pwn$ /domain:<domain>
Rubeus.exe asktgt /user:Pwn$ /aes256:<AES256KEY> /domain:<domain>
Rubeus.exe asktgs /targetuser:attacker_dMSA$ /service:krbtgt/<domain> /dmsa /opsec /ptt /nowrap /outfile:ticket.kirbi /ticket:<BASE64TGT>
```

Fill placeholders like `<AES256KEY>` and `<BASE64TGT>` with actual values from previous steps.

---

## Requirements

- RSAT Active Directory PowerShell module installed (works in Evil-WinRM or standard PowerShell).

---

## Installation

1. Clone or download the repository.
2. Import the script:
```
. .\Invoke-BadSuccessor.ps1
```

3. Enumerate vulnerable OUs:
```
Find-VulnerableOU
```

4. Run the attack chain:
```
Invoke-BadSuccessor
```

---

## ⚠️ Disclaimer

For educational and authorized testing only. Use only with explicit permission. The authors assume no liability for misuse.

---

## Author

- :skull: **B5null**


























