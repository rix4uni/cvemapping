Table of contents
=================

<!--ts-->
   * [CVE-2023-47119](#cve-2023-47119)
   * [Detailed analysis](#detailed-analysis)
   * [POC](#poc)
   * [Escalation ?](#escalation)
   * [LAB Setup](#lab-setup)


<!--te-->

# CVE-2023-47119
A POC for [CVE-2023-47119](https://nvd.nist.gov/vuln/detail/CVE-2023-47119) which is a vulnerability affecting [Discourse](https://github.com/discourse/discourse) versions prior to version 3.1.3 of the `stable` branch and version 3.2.0.beta3 of the `beta` and `tests-passed` branches. Some links can inject arbitrary HTML tags when rendered through the Onebox engine.

# Detailed analysis

Article : https://baadmaro.github.io/posts/Discourse-CVE-2023-47119-Building-a-CVE-POC-from-commits-changes/

# POC

- Payload : A link to a github issue with a label including an HTML injection in name. Example https://github.com/BaadMaro/test-discourse-github/issues/2

![image](https://github.com/BaadMaro/CVE-2023-47119/assets/72421091/b572c978-895e-4ec5-b223-4fc0da05f17f)

![image](https://github.com/BaadMaro/CVE-2023-47119/assets/72421091/28cae5f3-89e4-4ed6-9ddf-d6f702b17457)

![image](https://github.com/BaadMaro/CVE-2023-47119/assets/72421091/cdac2e11-5932-48fb-b3a5-4a5dc83741a1)


```html
<span style="display:inline-block;margin-top:2px;background-color: #B8B8B8;padding: 2px;border-radius: 4px;color: #fff;margin-left: 3px;">
          bug <h1>BaadMaro HTML Injection POC</h1>
        </span>
```

In fixed versions 

![image](https://github.com/BaadMaro/CVE-2023-47119/assets/72421091/2241bfb2-ba1a-4500-8aea-f929d474641c)

# Escalation

A bypass for the used XSS filters is needed https://github.com/discourse/discourse/security#xss 

# LAB Setup

To build Discourse 3.1.3 which is a vulnerable version, I used the docker compose file by bitnami https://hub.docker.com/r/bitnami/discourse/ 
- docker-compose.yml : https://raw.githubusercontent.com/bitnami/containers/main/bitnami/discourse/docker-compose.yml
- Modify the 2 images tag to 3.1.3 or any other vulnerable version `docker.io/bitnami/discourse:3.1.3`
- Change host to your preferable setup like 0.0.0.0 or your internal network IP address `DISCOURSE_HOST=0.0.0.0`
- You can also modify the port 80
- After modifying the file, run `docker-compose up -d`
- Few minutes you'll be able to see the discourse web server at your host port 80 
- App default login `user:bitnami123`

You can also use the official docker https://github.com/discourse/discourse_docker 
