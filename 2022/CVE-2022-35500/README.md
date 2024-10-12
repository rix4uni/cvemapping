# CVE-2022-35500
Stored Cross-site Scripting (XSS) in leave comment functionality in Amasty Blog Pro for Magento 2

## Description
The leave comment functionality in the Amasty Blog Pro 2.10.3 and 2.10.4 plugin for Magento 2 allows injection of JavaScript code in the `AmBlogLeaveComment` mutation in `name` parameter via GraphQL endpoint. The JavaScript code is executed when the victim (administrator) tries to remove the comment from the admin panel.

## Affected versions
< 2.10.5

## Advisory
Update Amasty Blog Pro for Magento 2 to 2.10.5 or newer.

## References
* https://amasty.com/blog-pro-for-magento-2.html
