# CVE-2019-17382 - Zabbix Authentication Bypass

A critical vulnerability discovered in Zabbix versions up to 4.4. The issue exists within the zabbix.php file when accessing the dashboard.view action with dashboardid=1. It enables attackers to bypass the login page, granting unauthorized access to the dashboard creation feature. Consequently, an attacker can create Dashboards, Reports, Screens, or Maps without the need for valid credentials (Username/Password), essentially operating anonymously.

# Vulnerability Impact

By exploiting this vulnerability, unauthorized elements (Dashboard/Report/Screen/Map) can be created, all of which remain accessible not only to the attacker but also to other users and administrators within the system.

# Vulnerability Identification

The vulnerability can be identified by accessing the zabbix.php file with the following parameters:

/zabbix.php?action=dashboard.view&dashboardid=1

# Steps to Reproduce

    Access the Zabbix interface.
    Directly navigate to /zabbix.php?action=dashboard.view&dashboardid=1 in a web browser.
    Observe the ability to create Dashboard, Report, Screen, or Map without valid login credentials.

# Mitigation

It is highly recommended to upgrade to a patched version of Zabbix beyond 4.4 to mitigate this vulnerability. Additionally, restrict access to the affected endpoint and consider implementing stricter authentication controls to prevent unauthorized access.

# Disclaimer

This PoC is only meant for educational purposes! You are responsible for your own actions.
