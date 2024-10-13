# Security breach project - Privilege escalation

The vulnerability is in Oracle Solaris, a product of Oracle Systems (component: XScreenSaver). The supported version that is affected is 11. It's an easily exploitable vulnerability which allows low privileged attackers with logon to the infrastructure where Oracle Solaris executes to compromise Oracle Solaris. While the vulnerability is in Oracle Solaris, attacks may significantly impact additional products.
Successful attacks of this vulnerability can result in takeover of Oracle Solaris. CVSS 3.0 Base Score 8.8

## Demonstration

## Demonstration steps

-launch: 'vagrant up' to download the environment (naturally takes some time : up to a couple of hours -it's vagrant whatchu gonna do  ¯\_(ツ)_/¯).

-Once the environment is ready, launch 'vagrant ssh'

## Good to know

-To create a file, we can only use nano, since the download already takes a lot of time, and we didn't want to burden the whole experiment with an install of vim or emacs.

```bash
nano exploit.sh
```

-The report is in French, it describes measures which could limit this type of breach, it also gives a detailed analysis of the breach and a detailed walk-through of what you should do in order to reproduce the breach. 
