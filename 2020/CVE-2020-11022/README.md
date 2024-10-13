# https-nj.gov---CVE-2020-11022
#### Vulnearability Report of the New Jersey official site
Potential XSS vulnerability in jQuery.htmlPrefilter and related methods.

Passing HTML from untrusted sources - even after sanitizing it - to one of jQuery's DOM manipulation methods (i.e. .html(), .append(), and others) may execute untrusted code.
# RECOMMENDATION
This problem is patched in jQuery 3.5.0; Therefore, it would only be necessary to update it.

To fix this bug without updating it, we can add the following code:
 
```
  jQuery.htmlPrefilter = function( html ) {
    return html;
  };
  ```
##### At least jQuery 1.12/2.2 or later is required to apply this workaround.
# REFERENCES
https://blog.jquery.com/2020/04/10/jquery-3-5-0-released/
https://jquery.com/upgrade-guide/3.5/

##### For more information
If you have any questions or comments about this advisory, search for a relevant issue in the [jQuery repo](https://github.com/jquery/jquery/issues). If you don't find an answer, open a new issue.
