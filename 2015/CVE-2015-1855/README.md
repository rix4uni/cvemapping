reproducer for CVE-2015-1855

how to reproduce it:

create the necessary infra-structure

```
$ bash 1.sh
```

set the vulnerable ruby (my system ruby is vulnerable)

```
$ rvm use system
$ ruby -v 1.rb
$ ruby 2.1.2p95 (2014-05-08 revision 45877) [x86_64-linux-gnu]
true  # true means vulnerable
```

set the fixed ruby

```
$ rvm use 2.3.0
$ ruby -v 1.rb
ruby 2.3.0p0 (2015-12-25 revision 53290) [x86_64-linux]
false
```
