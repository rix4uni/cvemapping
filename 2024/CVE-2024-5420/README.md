### Description
A vulnerability was found in utnserver Pro, utnserver ProMAX, and INU-100 version 20.1.22 and earlier, affecting the device description parameter in the web interface. 
This flaw allows stored cross-site scripting (XSS), enabling attackers to inject JavaScript code. The attack can be executed remotely by tricking victims into visiting a malicious website, 
potentially leading to session hijacking. This vulnerability is publicly disclosed and identified as CVE-2024-5420.

### USAGE
```bash
nuclei --target http://192.168.1.1:8080/ -t CVE-2024-5420.yaml
```

### Dork query
```bash
FOFA : title="utnserver Control Center"
```
```bash
SHODAN : SEH HTTP Server
```
