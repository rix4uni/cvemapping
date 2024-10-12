# VMware vCenter - CVE-2024-37081 Proof of Concept

## Descripción

Este repositorio contiene una prueba de concepto (PoC) para la vulnerabilidad CVE-2024-37081 en VMware vCenter. La vulnerabilidad se debe a una mala configuración en el archivo `/etc/sudoers` que permite la preservación de variables ambientales peligrosas al ejecutar comandos `sudo`. Esto puede ser aprovechado por atacantes para ejecutar comandos arbitrarios con privilegios de root.

## Vulnerabilidad

- **ID**: CVE-2024-37081
- **Descripción**: La mala configuración del parámetro `Defaults env_keep` en el archivo `/etc/sudoers` permite la propagación de variables ambientales peligrosas (`PYTHONPATH`, `VMWARE_PYTHON_PATH`, `VMWARE_PYTHON_BIN`, etc.) durante la ejecución de comandos `sudo`, lo que posibilita la ejecución de código arbitrario con privilegios de root.
- **Usuarios/Gruppos Afectados**:
  - `%operator` (grupo)
  - `%admin` (grupo)
  - `infraprofile` (usuario)
  - `vpxd` (usuario)
  - `sts` (usuario)
  - `pod` (usuario)

## Requisitos

- Python 3.x
- Permisos de sudo

## Instrucciones

1. Clona este repositorio:
    ```bash
    git clone https://github.com/Mr-r00t11/CVE-2024-37081.git
    cd CVE-2024-37081
    ```

2. Ejecuta el script PoC:
    ```bash
    python3 poc.py
    ```

## Contenido del Repositorio

- `poc.py`: Script en Python que demuestra la explotación de la vulnerabilidad.
- `README.md`: Este archivo.

## Detalles del Script

El script `poc.py` realiza los siguientes pasos:

1. **create_malicious_code()**: Crea un archivo Python malicioso en el directorio `/tmp/malicious/__init__.py` que ejecuta el comando `id` y guarda la salida en `/tmp/pwned`.
2. **execute_with_pythonpath()**: Establece la variable ambiental `PYTHONPATH` a `/tmp/malicious` y ejecuta un comando sudo para importar un módulo Python como el usuario `operator`.
3. **execute_with_vmware_python_path()**: Similar a `execute_with_pythonpath()`, pero usa la variable ambiental `VMWARE_PYTHON_PATH` y ejecuta el comando como el usuario `pod`.
4. **execute_with_vmware_python_bin()**: Crea un script shell malicioso, establece la variable ambiental `VMWARE_PYTHON_BIN` a este script, y ejecuta un comando sudo como el usuario `admin`.
5. **execute_with_sendmail()**: Ejecuta un comando sudo como el usuario `vpxd` para leer el archivo `/etc/shadow` usando `sendmail`.
6. **check_exploit_success()**: Verifica si el archivo `/tmp/pwned` ha sido creado, lo que indicaría que el código malicioso se ejecutó con éxito.

## Notas de Seguridad

Este script debe usarse únicamente en un entorno controlado y con fines educativos. La explotación de vulnerabilidades en sistemas sin autorización es ilegal y está penada por la ley. Asegúrate de tener permisos adecuados y de comprender completamente las implicaciones de ejecutar este tipo de código.

## Créditos

- **Investigador de Seguridad**: Matei “Mal” Badanoiu

## Licencia

Este proyecto está licenciado bajo los términos de la [MIT License](LICENSE).

