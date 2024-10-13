## Overview

md-to-pdf is a CLI tool for converting Markdown files to PDF.

Affected versions of this package are vulnerable to Remote Code Execution (RCE) due to utilizing the library gray-matter to parse front matter content, without disabling the JS engine.


### Usage: 

``` 
python3 cve-2021-23639.py targer_url command

```

### More

[Remote Code Execution (RCE) of md-to-pdf](https://security.snyk.io/vuln/SNYK-JS-MDTOPDF-1657880)
