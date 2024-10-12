# RCE-QloApps-CVE-2024-40318
A remote code execution (RCE) attack allow an attacker run code on a  computer. The ability to execute code could lead  to deploying additional malware or stealing sensitive data or even harm the server.

The remote code execution was discover in Qloapps version 1.6.0.0 while the application was being checked in the administrator panel, in the section “Modules  and services” where is possible to upload a modified module like “mailchimp-for-prestashop”(https://addons.prestashop.com/en/newsletter-sms/26957-mailchimp-for-prestashop.html”), this allowed to evade the php file upload restriction and get a remote code execution by modifing the file “cronjob.php” and accessing to it through the web browser.
