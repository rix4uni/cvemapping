# PoC Authentication Bypass MFA Really Simple Security WordPress Plugin

Accedemos a la página web de wordpress donde veremos que tiene MFA activado a través del plugin vulnerable:

![imagen](https://github.com/user-attachments/assets/0b6b5736-e7aa-45ba-b6f4-d2db7a45d9ee)

Debemos ejecutar la PoC y proporcionar los datos de acceso:


![imagen](https://github.com/user-attachments/assets/c551b296-6835-49b3-b844-4d532e4b53e2)

De forma automática, se abrirá el navegador mediante un archivo temporal .html dentro del panel de administración.

![imagen](https://github.com/user-attachments/assets/2de116bb-302b-4d6b-b12d-d986b162e9ee)

Para desplegar automáticamente un entorno vulnerable donde recrear este escenario, se puede utilizar el siguiente repositorio:

https://github.com/Trackflaw/CVE-2024-10924-Wordpress-Docker
