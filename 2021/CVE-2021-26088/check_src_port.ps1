# Initialize a new local connection to get the assigned port range of the current user

$tcpSocket = New-Object System.Net.Sockets.TcpClient

# Local open port
$destinationIpAddress = "127.0.0.1"
$destinationPort = 445

$tcpSocket.Connect($destinationIpAddress, $destinationPort)

Write-Output($tcpSocket.Client.LocalEndPoint)
$tcpSocket.Close()