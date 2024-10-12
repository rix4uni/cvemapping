# CVE-2024-41290
FlatPress CMS v1.3.1 1.3 was discovered to use insecure methods to  store authentication data

Additional Information:

FlatPress CMS version 1.3.1 insecurely stores authentication-related data, including usernames and hashed passwords, directly in client-side cookies. This practice exposes sensitive information to potential unauthorized access and manipulation by attackers.

Vendor of Product:

Insecure Storage of Authentication Data in Cookies

Affected Product Code Base:

FlatPress CMS version 1.3.1 - 1.3

Affected Component:

Cookie

Impact:

Usernames and hashed passwords are exposed in client-side cookies, which can be accessed or modified by unauthorized parties.

If an attacker gains access to these cookies, they can potentially impersonate users or decrypt hashed passwords offline

Discoverer:

Parag Bagul
