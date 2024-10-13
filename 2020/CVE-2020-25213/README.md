
## Description

The File Manager (wp-file-manager) plugin before 6.9 for WordPress allows remote attackers to upload and execute arbitrary PHP code because it renames an unsafe example elFinder connector file to have the .php extension. This, for example, allows attackers to run the elFinder upload (or mkfile and put) command to write PHP code into the wp-content/plugins/wp-file-manager/lib/files/ directory. This was exploited in the wild in August and September 2020.


## Demo

```bash
python3 exploit.py url command
python3 exploit.py http://wordpressite.com/ id
```


## Authors

- [@BLY](https://www.github.com/bly-coder)



## Deployment

To deploy:

```bash
  git clone https://github.com/BLY-Coder/Python-exploit-CVE-2020-25213
  run with python3
```

