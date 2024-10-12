# Metabase Pre-Auth RCE (CVE-2023-38646) POC

This is a script written in Python that allows the exploitation of the **Metabase's** software security flaw described in **CVE-2023-38646.** The system is vulnerable in versions preceding **0.46.6.1**, in the open-source edition, and preceding **1.46.6.1**, in the enterprise edition.

## Usage

The script needs the **target URL**, the **setup token** and a **command** that will be executed. The setup token can be obtained through the ```/api/session/properties``` endpoint. Copy the value of the ```setup-token``` key.

![setup-token value](https://i.ibb.co/N22FgN6/setup-token.png)

The **command** will be executed on the target machine with the intention of obtaining a **reverse shell**. You can find different options in [RevShells](https://revshells.com). Having the **setup-token** value and the **command** that will be executed, you can run the script with the following command:

```python3 main.py -u http://[targeturl] -t [setup-token] -c "[command]"```

![script demo](https://iili.io/J2pd3Pe.gif)

## References

[Chaining our way to Pre-Auth RCE in Metabase (CVE-2023-38646)](https://blog.assetnote.io/2023/07/22/pre-auth-rce-metabase/)

[Reproducing CVE-2023-38646: Metabase Pre-auth RCE](https://blog.calif.io/p/reproducing-cve-2023-38646-metabase)
