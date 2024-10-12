# CVE-2023-27163

> [!WARNING]  
> This is an educational project, I am not responsible for any use

# Exploit

Exploit for CVE-2023-27163, an SSRF vulnerability discovered in request-baskets in all versions below 1.2.1. This vulnerability allows attackers to exploit the /api/baskets/{name} component via a manipulated API request.

# What is it and how does it work?

Request-baskets is a web application created to collect and register requests in a path, called a basket. When creating it, the user can specify another server to forward the request to. [to learn more visit the official website](https://github.com/darklynx/request-baskets)

For example: The server is hosting Request-baskets on port `55555` and an http page on port 80 which can only be accessed from localhost. By creating a basket that forwards to `http://127.0.0.1:80`, the attacker can access the web server on port `80` from the attacking machine.

# Usage

```zsh
wget https://raw.githubusercontent.com/Rubioo02/CVE-2023-27163/main/CVE-2023-27163.sh
chmod +x CVE-2023-27163.sh
./CVE-2023-27163.sh -t <TARGET_URL> -a <ATTACKER_URL>
```

# BLOG
<https://rubioo02.github.io/>
