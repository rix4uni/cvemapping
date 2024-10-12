# CVE-2023-49314
Asana Desktop 2.1.0 on macOS allows code injection because of specific Electron Fuses. There is inadequate protection against code injection through settings such as RunAsNode and  enableNodeCliInspectArguments, and thus electroniz3r can be used to perform an attack.

![Captura de Tela 2023-11-27 às 20 07 12](https://github.com/louiselalanne/CVE-2023-49314/assets/100588945/070cd9e1-2018-4b39-aa1f-a71fdaaa538e)

There is a tool designed to automate the process of searching for vulnerabilities in electron: https://github.com/r3ggi/electroniz3r

- We'll check if the application is vulnerable:
 
![Captura de Tela 2023-11-27 às 19 56 55](https://github.com/louiselalanne/CVE-2023-49314/assets/100588945/4c088eeb-2061-4f1b-9a83-a7a9d03fd16c)

- Now we can inject a bind shell:

![Captura de Tela 2023-11-27 às 19 59 19](https://github.com/louiselalanne/CVE-2023-49314/assets/100588945/91108b25-385d-436f-a76a-2315ad1d1cec)

- And we got our shell

![Captura de Tela 2023-11-27 às 19 59 59](https://github.com/louiselalanne/CVE-2023-49314/assets/100588945/112212d6-c78e-4fa8-8192-305ef220e194)

- To undestand more about Electron Desktop Apps:
https://www.electronjs.org/docs/latest/tutorial/fuses
