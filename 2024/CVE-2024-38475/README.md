# CVE-2024-38475 POC

**Credit**: All credit to this guy: https://blog.orange.tw/ and https://x.com/orange_8361 all i did was make a POC script from his research.

**Introduction** : Improper escaping of output in mod_rewrite in Apache HTTP Server 2.4.59 and earlier allows an attacker to map URLs to filesystem locations that are permitted to be served by the server but are not intentionally/directly reachable by any URL, resulting in code execution or source code disclosure. Substitutions in server context that use a backreferences or variables as the first segment of the substitution are affected.  Some unsafe RewiteRules will be broken by this change and the rewrite flag "UnsafePrefixStat" can be used to opt back in once ensuring the substitution is appropriately constrained.

I highly recommend staying with the wordlists i've used when developing this tool. The tool itself is work in progress, and might need modifications due to the url handling of files and directories. I've used `raft-medium-files.txt` and `raft-medium-directories.txt` while developing and testing the vulnerbillity on my own systems.

