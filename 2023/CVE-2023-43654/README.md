<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/OligoCyberSecurity/ShellTorchChecker/assets/8081679/e35ee9a8-425c-47d1-b246-13e19e450860">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/OligoCyberSecurity/ShellTorchChecker/assets/8081679/a2d9f351-3e69-4d67-b3d1-c0a982cb89cf">
  <img height=130px  alt="ShellTorch Logo" src="https://github.com/OligoCyberSecurity/ShellTorchChecker/assets/8081679/a2d9f351-3e69-4d67-b3d1-c0a982cb89cf">
</picture>

## ShellTorch Checker Tool

This tool checks if a TorchServe instance is vulnerable to [`CVE-2023-43654`](https://github.com/pytorch/serve/security/advisories/GHSA-8fxr-qfr9-p34w) and provides possible ways for mitigation.

For more details please see our full report at https://www.oligo.security/blog/shelltorch-torchserve-ssrf-vulnerability-cve-2023-43654

To run the tool, execute the following command:

```bash
bash <(curl https://raw.githubusercontent.com/OligoCyberSecurity/ShellTorchChecker/main/ShellTorchChecker.sh) $TORCHSERVE_IP
```

## Disclaimer
```
By using this tool, you acknowledge and agree that it is provided "as is" without
warranty of any kind, either express or implied. Oligo and any contributors shall not be held
liable for any direct, indirect, incidental, or consequential damages or false results arising
out of the use, misuse, or reliance on this tool.
You are solely responsible for understanding the output and implications of using this tool
and for any actions taken based on its findings.
Use at your own risk.
```
