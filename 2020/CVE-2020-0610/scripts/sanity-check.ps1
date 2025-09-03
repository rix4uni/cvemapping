# Verifies RD Gateway role presence and UDP/3391 firewall rule
param()
$rdgRole = (Get-WindowsFeature Remote-Desktop-Gateway).Installed
$rule = Get-NetFirewallRule -DisplayName "RDG-UDP-3391" -ErrorAction SilentlyContinue
Write-Host "RD Gateway role installed: $rdgRole"
if ($rule) {
  $enabled = ($rule.Enabled -eq True)
  Write-Host "UDP/3391 firewall rule present: True, enabled: $enabled"
} else {
  Write-Host "UDP/3391 firewall rule present: False"
}
