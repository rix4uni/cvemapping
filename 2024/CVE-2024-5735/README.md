# CVE-2024-5735
AdmirorFrames Joomla! Extension < 5.0 - Full Path Disclosure

## Timeline
- Vulnerability reported to vendor: 26.01.2024
- New fixed 5.0 version released: 06.06.2024
- Public disclosure: 28.06.2024

## Description

Full Path Disclosure vulnerability in AdmirorFrames Joomla! Extension in `afHelper.php` file which uses value of `JPATH_BASE` directly when constructing path to image. According to Joomla! documentation `JPATH_BASE` is defined as:
```
The path to the installed Joomla! site
```

The vulnerability exists in `afHelper.php` file:
```
 $this->params['templates_BASE'] = JPATH_BASE . DIRECTORY_SEPARATOR . 'plugins' . DIRECTORY_SEPARATOR .
             'content' . $path . 'templates' . DIRECTORY_SEPARATOR;
```

This issue was caused by direct usage of `JPATH_BASE` variable when constructing image path. This problem has been fixed in AdmirorFrames Joomla! Extension at version 5.0.

## Affected versions
< 5.0 

## Advisory
Update AdmirorFrames Joomla! Extension to version 5.0 or newer.

### References
* https://github.com/vasiljevski/admirorframes/issues/3
* https://cert.pl/en/posts/2024/06/CVE-2024-5735/
* https://cert.pl/posts/2024/06/CVE-2024-5735/
* https://nvd.nist.gov/vuln/detail/CVE-2024-5735
