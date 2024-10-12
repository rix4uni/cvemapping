# CVE-2023-6000 PoC

 ## How does this detection method work?
 
This template looks at the following path: /wp-content/plugins/popup-builder/readme.txt

Based on the Stable Tag listed, if the version is prior to `4.2.3` then it is considered to be vulnerable.

 ## How do I run this script?

1. Download Nuclei from [here](https://github.com/projectdiscovery/nuclei)
2. Copy the template to your local system
3. Run the following command: `nuclei -u https://yourHost.com -t template.yaml` 

## References

- https://nvd.nist.gov/vuln/detail/CVE-2023-6000
- https://www.bleepingcomputer.com/news/security/hackers-exploit-wordpress-plugin-flaw-to-infect-3-300-sites-with-malware/


## Disclaimer

Use at your own risk, I will not be responsible for illegal activities you conduct on infrastructure you do not own or have permission to scan.


# Contact

If you have any questions feel free to reach out to me on [Signal](https://signal.me/#eu/0Qd68U1ivXNdWCF4hf70UYFo7tB0w-GQqFpYcyV6-yr4exn2SclB6bFeP7wTAxQw) or via email: rishi@rxerium.com.