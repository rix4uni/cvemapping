# Elasticsearch 1.4.0 &lt; 1.4.2 Remote Code Execution

Elasticsearch is a distributed, RESTful search and analytics engine capable of solving a growing number of use cases. As the heart of the Elastic Stack, it centrally stores your data so you can discover the expected and uncover the unexpected.

## Vulnerable environment

To setup a vulnerable environment for your test you will need [Docker](https://docker.com) installed, and just run the following command:

    docker build -t vuln/cve-2015-1427 .
    docker run --rm -it -p 9200:9200 vuln/cve-2015-1427

And it will spawn a vulnerable web application on your host on `9200` port

## Vulnerable code

The bug is found in the REST API, which does not require authentication, where the search function allows groovy code execution and its sandbox can be bypassed using `java.lang.Math.class.forName` to reference arbitrary classes. It can be used to execute arbitrary Java code. The bug is found in the REST API, which does not require authentication, where the search function allows groovy code execution and its sandbox can be bypassed using `java.lang.Math.class.forName` to reference arbitrary classes. It can be used to execute arbitrary Java code.

## Exploit

To exploit this target just run:

    ./exploit.sh host:port

If you are using this vulnerable image, you can just run:

    ./exploit.sh 127.0.0.1:9200
    [+] CVE-2015-1427 exploit by t0kx
    [+] Exploiting 127.0.0.1:9200
    [+] Trigger Payload...
    [+] Running whoami: root
    [+] Done

## Credits

This flaw was found by the Cisco Systems Information Security Team and Cameron Morris.

## Disclaimer

This or previous program is for Educational purpose ONLY. Do not use it without permission. The usual disclaimer applies, especially the fact that me (t0kx) is not liable for any damages caused by direct or indirect use of the information or functionality provided by these programs. The author or any Internet provider bears NO responsibility for content or misuse of these programs or any derivatives thereof. By using these programs you accept the fact that any damage (dataloss, system crash, system compromise, etc.) caused by the use of these programs is not t0kx's responsibility.
