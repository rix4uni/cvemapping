
# CVE-2025-47175 - Microsoft PowerPoint Use-After-Free (UAF) Remote Code Execution PoC

## Overview

This repository contains a Proof of Concept (PoC) exploit for the **CVE-2025-47175** vulnerability found in Microsoft PowerPoint.  
The vulnerability is a Use-After-Free (UAF) bug that allows an attacker to execute arbitrary code by tricking a user into opening a specially crafted PPTX file.

---

## Description

- **Vulnerability:** Use-After-Free (UAF) in Microsoft PowerPoint  
- **CVE ID:** CVE-2025-47175  
- **Affected Versions:** Microsoft PowerPoint 2019 and Office 365 versions prior to June 2025 Patch (KB5002689)  
- **Attack Vector:** Local — requires victim to open a crafted PPTX file  
- **Impact:** Remote Code Execution (RCE)  

This PoC script generates a malicious PPTX file designed to trigger the UAF vulnerability. Opening the generated file in a vulnerable PowerPoint version may lead to arbitrary code execution.

---

## Usage

```bash
python3 exploit_cve2025_47175.py [options]
```

### Options

| Option          | Description                               | Default                              |
|-----------------|-------------------------------------------|------------------------------------|
| `-o`, `--output` | Output PPTX filename                      | `exploit_cve_2025_47175.pptx`      |
| `-i`, `--id`     | Shape ID (integer)                        | `1234`                             |
| `-n`, `--name`   | Shape Name (string)                       | `MaliciousShape`                   |
| `-t`, `--text`   | Trigger text inside the slide             | `This content triggers CVE-2025-47175 UAF vulnerability.` |

### Example

```bash
python3 exploit_cve2025_47175.py -o evil.pptx -i 5678 -n "BadShape" -t "Triggering CVE-2025-47175 now!"
```

---

## Disclaimer

This PoC is for educational and research purposes only. Unauthorized use against systems without explicit permission is illegal. The author is not responsible for any misuse of this code.

---

## Author

Mohammed Idrees Banyamer  
- Instagram: [@banyamer_security](https://instagram.com/banyamer_security)  
- GitHub: [https://github.com/mbanyamer](https://github.com/mbanyamer)  

---

## References

- [Microsoft Security Update Guide](https://msrc.microsoft.com/update-guide)  
- [Exploit-DB](https://www.exploit-db.com/?author=12252)  
