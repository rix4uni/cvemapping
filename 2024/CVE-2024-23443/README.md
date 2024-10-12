# Proof of Concept (POC)
CVE-2024-23443

# hp_bios_osquery
Add osqery extension HP BIOS WMI to Elastic Agent 

# Dependencies

- pip install pywin32
- pip install osquery
- pip install pyinstaller

# Build

```
pyinstaller --onefile hp_bios_enumeration.py
```

# Install

1. Copy extension to Elastic agent location
   
   ``copy .\hp_bios_enumeration.exe "C:\Program Files\Elastic\Agent\data\elastic-agent-XXXXXX\components\"``
   
2. Update Elastic osquery auto_load file

   ``"C:\Program Files\Elastic\Agent\data\elastic-agent-XXXXXX\components\hp_bios_enumeration.exe" | Out-File "C:\Program Files\Elastic\Agent\data\elastic-agent-XXXXXX\run\osquery-default\osquery\osquery.autoload" -Append``

3. Restart agent

4. Confirm extension is loaded

   ``osqueryi``

    ``osquery> SELECT * FROM hp_bios_enum;``

   | name                                | possible_values                                                 | current_value                       |
   |-------------------------------------|-----------------------------------------------------------------|-------------------------------------|
   | System Management Command           | Disable, Enable                                                 | Enable                              |
   | Fast Boot                           | Disable, Enable                                                 | Enable                              |
   | BIOS Rollback Policy                | Unrestricted Rollback to older BIOS, Restricted Rollback to older BIOS | Unrestricted Rollback to older BIOS |
   | Audio Alerts During Boot            | Disable, Enable                                                 | Enable                              |
    
