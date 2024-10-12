# Broken Access Control Vulnerability was discoverd in Sourcecodester Online Eyewear Shopping Website ID,Cart ID Manipulation Leads to Unwanted Item Addition and Deletion into User's Cart

---

## CVE-2024-8949

---

Vendor: Sourcecodester [https://www.sourcecodester.com/php/16089/online-eyewear-shop-website-using-php-and-mysql-free-download.html]

Reference: https://github.com/gurudattch/

Product: Online Eyewear Shop Version: 1.0



Vulnerability Overview:

The Online Eyewear Shop version 1.0, developed by Sourcecodester, is vulnerable to a cart ID,ID manipulation vulnerability. This vulnerability allows an attacker to add or delete unwanted items to other users' carts by modifying the cart ID.

Vulnerability Details:
---

  -  Attack Vector: An attacker can exploit this vulnerability by tampering with the cart ID, ID which is likely stored in a cookie or a parameter in the URL.
  -  Impact: An attacker can add or delete items from other users' carts, leading to unwanted changes to their shopping carts. This can result in financial losses for the users and damage to the reputation of the Online Eyewear Shop.
  -  Exploitation: An attacker can exploit this vulnerability by intercepting and modifying the cart ID, allowing them to access and manipulate other users' carts.


---

Exploitaion
---

1. Login with **User1** go add some item in cart and click on cart
2. Turn on BurpSuite and intercept this request
3. Click on **+** to increase quantity

![image](https://github.com/gurudattch/CVEs/blob/main/assets/19.png)

4. Change the Cart_id of user1 to user2's cart id logout and login with **User2** Observer the Item added to the **Users2's** Cart

![image](https://github.com/gurudattch/CVEs/blob/main/assets/20.png)

> Similarly this functionallity vulnerable for delete item

1. Click on Delete item icon in cart and intercept the request change the Cart ID and from **id** parameter
   
![image](https://github.com/gurudattch/CVEs/blob/main/assets/21.png)

2. login into the victim user's account and observe the empty cart

![image](https://github.com/gurudattch/CVEs/blob/main/assets/22.png)
