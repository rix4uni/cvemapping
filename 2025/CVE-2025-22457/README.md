# ivantiunlocker
Prevent CVE-2025-22457 and other security problems with Juniper/Ivanti Secure Connect SSL VPN

Many security issues around SSL VPN devices recently. You can't feel safe anymore. And then there is CVE-2025-22457 !
Read the story behind it : https://labs.watchtowr.com/is-the-sofistication-in-the-room-with-us-x-forwarded-for-and-ivanti-connect-secure-cve-2025-22457/
POST / HTTP/1.1
X-Forwarded-For: 1111111111111111111111111111111...
will open the door to your appliance !

As we have PSA3000 and there is no firmware update available for fixing this problem it is obvious that Ivanti wants to push you to buy
new devices like ISA6000 for 10.000 USD+. I guess you buy that and then the next security issues will happen anyway.

But we found a way to get out of the hamster wheel. You need to have a network gate in front of the SSL VPN appliance by solid firewall rules.
You can do this the hard way with an additional OpenVPN or wireshark server. Or you can do it in a soft manner which is more comfortable for your visitors.
Our approach is easy to implement, easy to use and highly efficient because it prevents any attacker from even detecting you or having possibility to connect to the
appliance.

The gateway is a simple python written webserver (listens on HTTPS port 443 instead of SSL VPN) which presents the visitor a password entry box. When correct passwort
is entered then the visitor's IP gets FORWARD/PREROUTING firewall entries and he then can immediately access the SSL VPN device with same URL/port.

This is just one possible approach. You also could have user/password combinations, a pin pad, user certificates, use 2FA Authelia, etc...
But in the end you need to handle it by firewall rules because SSL VPN devices don't like it if you terminate SSL/TLS elsewhere.
Also only this way you can hide from attackers completely which prevents any future CVE security breach problem.
