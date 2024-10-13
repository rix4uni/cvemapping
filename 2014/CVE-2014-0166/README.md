##POC&EXP of CVE-2014-0166
####WordPress < 3.8.2 cookie forgery vulnerability

**Details of this vulnerability can be found at [here](http://www.ettack.org/wordpress-cookie-forgery/)**

There are three files:

* _wp\_zero\_cookie\_generator.php_
    * **POC to verify this vulnerability.**  
        * It **won't** send any requests, just a local brute-forcer.  
        * Redefine variables to supply info and it will try to find out a **_zero cookie_**.

* _zeroCatcher.py_
    * **Multiprocessing POC written in python**
        * The same as _wp\_zero\_cookie\_generator.php_.
        * Except that multiprocessing is applied for better performance.
        
* _cookieForger.py_
    * **Multi thread remote EXP**  
        * Read the source code and you will understand **_everything_** about it.  
