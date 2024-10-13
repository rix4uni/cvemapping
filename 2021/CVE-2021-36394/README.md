# CVE-2021-36394-Pre-Auth-RCE-in-Moodle
### Vulnerability Introduction

`Moodle` is the most popular learning management system in the world. Start creating your eLearning website in minutes!

An unauthorized remote code execution vulnerability exists in the `Shibboleth` authentication module of `Moodle`. This is widely used in universities to allow students from one university to authenticate with other universities, allowing them to take external courses and have fun with others.



### Environment setup

````
git clone https://github.com/lavclash75/CVE-2021-36394-Pre-Auth-RCE-in-Moodle.git
cd "CVE-2021-36394 Pre-Auth RCE in Moodle"
docker-compose up -d
````

Then go to `docker` and change the file `/var/www/html/moodle-3.11.0/config.php`

````
$CFG->wwwroot = 'http://127.0.0.1';
````

Change the link above to your own, it must be a real address


