# CVE-2022-36433
Cross-site Scripting (XSS) in blog-post creation functionality in Amasty Blog Pro for Magento 2

## Description
The blog-post creation functionality in the Amasty Blog Pro 2.10.3 plugin for Magento 2 allows injection of JavaScript code in the `short_content` and `full_content` fields, leading to XSS attacks against admin panel users via posts/preview or posts/save.

Vulnerable endpoints which are the injection points for the parameters mentioned above:
* POST /admin/amasty_blog/posts/preview/key/{some_key}/?isAjax=true
* POST /admin/amasty_blog/posts/save/key/{some_key}/back/edit

## Affected versions
< 2.10.5

## Advisory
Update Amasty Blog Pro for Magento 2 to 2.10.5 or newer.

## References
* https://amasty.com/blog-pro-for-magento-2.html
