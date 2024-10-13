# Subrion CMS 4.2.1 - Cross Site Request Forgery (CSRF) (Add Administrator user)
# Description
Subrion CMS is easy to install and simple to manage. Use it as a stand-alone application or in conjunction with other applications to create entry level sites, mid-sized or large sites.

Cross Site Request Forgery (CSRF) vulnerability exists in Intelliants Subrion CMS v4.2.1 via the Members administrator function, which could allows a remote unauthenticated malicious user send an authorised request to victim and successfully create an arbitrary administrator user.

**Date**: 27-02-2022 \
**Software Link:** https://subrion.org \
**Exploit Author**: HaMM0nz \
**CVE**: CVE-2020-18326 \
**Category:** Web Application

# Proof of Concept
1. Craft the HTML and host the link in web application. (Please refer CVE-2020-18326.html)
2. Send the link to the victim.
3. A new administrator user will be created with the name "admincsrf". 

# Timeline
**Discovery and report** : 24 June 2019 \
**CVE ID was assigned** : 11 Aug 2021 \
**Public** : 27 February 2022
# Solution
Consider complying to the OWASP's CSRF prevention guidelines. (https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
