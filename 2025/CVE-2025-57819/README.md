# CVE-2025-57819

Overview of this vulnerability quoted from @jfinstrom [here](https://gist.github.com/jfinstrom/60011630ed586a79f5b9c78313e0d708#file-freepbx-vulnerability-aug-2026-md)
> - Around 2025-08-21 multiple FreePBX systems began showing errors and later confirmed compromises.
> - Vendor (Sangoma/FreePBX Security Team) published an advisory on 2025-08-26 urging administrators to restrict public access to the Administrator Control Panel and offering EDGE module fixes.
> - The vulnerability is associated with the commercial Endpoint Manager (Endpoint) and appears to be an unauthenticated privilege escalation/RCE that can be exploited when the Administrator UI is exposed to hostile networks.
> - The EDGE fix prevents new exploitation but does not clean already-compromised systems.

## How does this detection method work?

This template sends a request to the FreePBX admin panel, extracts the version, and flags it as vulnerable if it falls within the affected version ranges of the newly disclosed zero-day (16.0.0.0–16.0.88.19 or 17.0.0.0–17.0.2.31).

## How do I run this script?

1. Download Nuclei from [here](https://github.com/projectdiscovery/nuclei)
2. Copy the template to your local system
3. Run the following command: `nuclei -u https://yourHost.com -t template.yaml` 

## References

- https://community.freepbx.org/t/endpointmanager-aug-2025-zero-day/107215
- https://www.bleepingcomputer.com/news/security/freepbx-servers-hacked-via-zero-day-emergency-fix-released/


## Disclaimer

Use at your own risk, I will not be responsible for illegal activities you conduct on infrastructure you do not own or have permission to scan.

## Share This Project

<div align="center">
  <a href="https://twitter.com/intent/tweet?text=Check%20out%20this%20CVE%20detection%20template%20by%20@rxerium!&url=https://github.com/rxerium/poc-template" target="_blank">
    <img src="https://img.shields.io/badge/🐦%20Share%20on-Twitter-lightgrey?style=flat&logo=twitter&logoColor=1DA1F2" alt="Share on Twitter"/>
  </a>
  <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://github.com/rxerium/poc-template" target="_blank">
    <img src="https://img.shields.io/badge/💼%20Share%20on-LinkedIn-lightgrey?style=flat&logo=linkedin&logoColor=0077B5" alt="Share on LinkedIn"/>
  </a>
  <a href="mailto:?subject=CVE%20Detection%20Template&body=Check%20out%20this%20interesting%20CVE%20detection%20template%20by%20rxerium:%20https://github.com/rxerium/poc-template" target="_blank">
    <img src="https://img.shields.io/badge/%20Share%20via-Email-lightgrey?style=flat&logo=gmail&logoColor=D14836" alt="Share via Email"/>
  </a>
</div>

---

## Contact

Feel free to reach out via [Signal](https://signal.me/#eu/0Qd68U1ivXNdWCF4hf70UYFo7tB0w-GQqFpYcyV6-yr4exn2SclB6bFeP7wTAxQw) if you have any questions.
