# CVE-2022-35501
Stored Cross-site Scripting (XSS) in blog-post creation functionality in Amasty Blog Pro for Magento 2

## Description
The post creation functionality in the Amasty Blog Pro 2.10.3 and 2.10.4 plugin for Magento 2 allows injection of JavaScript code in the `title` field, leading to XSS attacks against admin panel users via duplicate post function, which used the data.title field and executed JavaScript code.

Vulnerable endpoint which is the injection point for the parameter mentioned above:
* POST /admin/amasty_blog/posts/save/key/{some_key}/

## Affected versions
< 2.10.5

## Advisory
Update Amasty Blog Pro for Magento 2 to 2.10.5 or newer.

## References
* https://amasty.com/blog-pro-for-magento-2.html
