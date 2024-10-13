Write-Output "Locking Global\PGHOOK mutexes"
$n = 65532
$x = New-Object System.Collections.ArrayList
for ($process_id = 1000; $process_id -le $n; $process_id+=4) {
    $CreatedMutex = ""
	try{
		$Mutex = New-Object -TypeName system.threading.mutex($true, "Global\PGHOOK$process_id", [ref] $CreatedMutex)
		$x.Add($mutex) >$null 2>&1
	}
	catch{}
}
Write-Output "Locked Global\PGHOOK mutexes available (from PIDs from 1000 to $n)"
