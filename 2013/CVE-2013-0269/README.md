heroku-CVE-2013-0269
===

Inspect all of your heroku apps to see if they are running a vulnerable version of JSON

Background
---

A [security vulnerability](https://groups.google.com/forum/#!topic/rubyonrails-security/4_YvCpLzL58/discussion) has been found in the Ruby
JSON gem. This is the root cause for the recently-announced MySQL
injection issue in Rails. A new release of the JSON gem is available.

Developers can get a full list of all your affected Heroku
applications by running [this
script](https://github.com/heroku/heroku-CVE-2013-0269/blob/master/heroku-CVE-2013-0269.rb).
The following JSON versions have been patched and deemed safe from
this exploit:

- 1.7.7
- 1.6.8
- 1.5.5

**If you do not upgrade, an attacker may be able to execute arbitrary
  SQL queries on your application's MySQL database. Heroku recommends
  upgrading to a patched version immediately.**

Instructions
---

* git clone git@github.com:heroku/heroku-CVE-2013-0269.git
* cd heroku-CVE-2013-0269
* ruby heroku-CVE-2013-0269.rb

PGP Signature
---
The Heroku Security Team's PGP key is available at [https://policy.heroku.com/security](https://policy.heroku.com/security)
