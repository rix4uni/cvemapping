# CVE-2022-36432
Cross-site Scripting (XSS) in Preview functionality in Amasty Blog Pro for Magento 2

## Description

The Preview functionality in the Amasty Blog Pro 2.10.3 plugin for Magento 2 uses `eval` unsafely. This allows attackers to perform Cross-site Scripting attacks on admin panel users by manipulating the generated preview application response.

The vulnerability is present in `blog/view/base/web/js/adminhtml/preview.js` file.

In references you can find a similar issue in Magento 2 in which they fixed the problem.

## Affected versions
< 2.10.5

## Advisory
Update Amasty Blog Pro for Magento 2 to 2.10.5 or newer.

### References
* https://github.com/magento/magento2/issues/377
* https://amasty.com/blog-pro-for-magento-2.html
