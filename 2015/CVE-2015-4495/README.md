# CVE-2015-4495
Exploit for CVE-2015-4495 / mfsa2015-78

## How to use
Add your logic in the `parse_directory_listing` function.

## Usage
```bash
$ git clone https://github.com/vincd/CVE-2015-4495.git
$ cd CVE-2015-4495
$ python -m SimpleHTTPServer
```

Then open an unpatch Firefox (version < 39.0.3). A popup should spawn with the content of `/`.

# Credits
http://paste.ubuntu.com/12030863/
