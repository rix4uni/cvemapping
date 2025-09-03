# Adds Windows Firewall rule for RD Gateway UDP transport on port 3391
param()
$ruleName = "RDG-UDP-3391"
if (-not (Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue)) {
  New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Protocol UDP -LocalPort 3391 -Action Allow | Out-Null
  Write-Host "Created firewall rule: $ruleName"
} else {
  Write-Host "Firewall rule already exists: $ruleName"
}
