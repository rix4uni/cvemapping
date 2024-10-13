heroku-CVE-2013-0333
===

Inspect all of your heroku apps to see if they are running a vulnerable version of Rails

Background
---

A [serious security
vulnerability](http://weblog.rubyonrails.org/2013/1/28/Rails-3-0-20-and-2-3-16-have-been-released/)
has been found in the [Ruby on Rails](http://rubyonrails.org)
framework. This exploit affects nearly all applications running Rails
versions 2.3 and 3.0, and a patch has been made available.

Rails developers can get a full list of all your affected Heroku applications by running [this script](https://github.com/heroku/heroku-CVE-2013-0333/blob/master/heroku-CVE-2013-0333.rb). The following Rails versions have been patched and deemed safe from this exploit:

- 3.0.20
- 2.3.16
- 3.2.x
- 3.1.x


**If you do not upgrade, an attacker can trivially gain access to your
  application, its data, and run arbitrary code or commands. Heroku
  recommends upgrading to a patched version immediately.**

Instructions
---

```sh
$ git clone git@github.com:heroku/heroku-CVE-2013-0333.git
$ cd heroku-CVE-2013-0333
$ ruby heroku-CVE-2013-0333.rb
```

PGP Signature
---
The Heroku Security Team's PGP key is available at [https://policy.heroku.com/security](https://policy.heroku.com/security)
