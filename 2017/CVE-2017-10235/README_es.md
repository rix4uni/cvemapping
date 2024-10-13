# CVE-2017-10235: Resumen del *buffer overflow* en el emulador de dispositivos de VirtualBox E1000


## Introducción

En este repositorio se encuentra una descripción técnica y prueba de concepto de una vulnerabilidad encontrada en VirtualBox v5.1.22 (solucionada en v5.1.24), específicamente en el componente de emulación de dispositivos en el *guest*, `DevE1000`, en la función `e1kFallbackAddToFrame`. Esta vulnerabilidad deriva en un *buffer overflow* en el *host* cuando el sistema operativo del *guest* es controlado por un atacante.

La vulnerabilidad fue reconocida por Oracle en el [CPU de Julio de 2017](http://www.oracle.com/technetwork/security-advisory/cpujul2017-3236622.html#AppendixOVIR) donde se emitió el [CVE-2017-10235](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-10235).

La vulnerabilidad fue comprobada tanto con un *host* de Linux (Ubuntu 16.04) como de Windows (v8.1), corriendo un sistema operativo Linux (también Ubuntu 16.04) en el *guest*, pero la vulnerabilidad podría explotarse con otras  combinaciones distintas de sistemas operativos para el *host* y el *guest*. En todos los escenarios de prueba se asume la configuración de red por defecto: solo un adaptador de red en modo NAT (opción **attached to NAT**) del tipo **Intel PRO/1000 MT Desktop (82540EM)**.

Dado que estructuras de control (que incluyen punteros a funciones) pueden ser sobreescritas con datos controlados por el atacante, es prudente asumir que podría lograrse ejecución de código remoto en muchos escenarios posibles. Oracle asignó un puntaje bajo para el CVSS de esta vulnerabilidad porque consideró que tenía un riesgo de confidencialidad nulo, y uno bajo para integridad, lo que a nuestra consideración no refleja todo el potencial de esta vulnerabilidad para comprometer al usuario (una explicación más detallada de esta potencialidad está dada en el [informe completo en inglés](./README.md#possible-rce)).


## Prueba de concepto

Dado que la configuración necesaria del adaptador de red para explotar esta vulnerabilidad no es para nada trivial, y para evitar desarrollar un *driver* especial para las pruebas, se modificó el *driver* de un *kernel* genérico de Linux para poder generar los paquetes de datos y de control para que suceda el *buffer overflow*. La versión modificada del *kernel* esta disponible para [descargar][poc_download] desde este repositorio. Fue probada con un *guest* de Ubuntu 16.04, causando un *crash* tanto en un *host* de Linux como Windows (una descripción más detallada en inglés se encuentra [acá](./poc/)).


## Soluciones posibles

La vulnerabilidad fue arreglada en el [Changeset 67974][Changeset_67974]. Los chequeos de seguridad en forma de `Assert` en `e1kFallbackAddToFrame` fueron convertidos a chequeos explícitos en forma de `if` (similares a los ya existentes en la función `e1kAddToFrame`), que de esta manera permanecen activos en la versión final que descarga el usuario.


## Terminología en inglés

* *Host* (anfitrión): La máquina donde se instala VirtualBox.

* *Guest* (huésped): La máquina emulada dentro de VirtualBox que puede tener un sistema operativo distinto al del *host*.

* *Buffer overflow*: Un error en la programación que puede derivar en que el programa sobreescriba por fuera de los límites de los de donde debería, pudiendo pisar información del sistema con datos externos controlados por el atacante.

* *Driver*: Componente del sistema operativo que se encarga de manejar los dispositivos de la máquina.

* *Kernel*: Componente central del sistema operativo.

* *Crash*: Situación en la cual el estado actual del sistema operativo se corrompe a nivel tal que resulta inusable (e.g., pantalla azul de Windows).

[poc_download]: https://github.com/fundacion-sadosky/vbox_cve_2017_10235/releases/download/v1.0/linux-image-4.8.0-vbox-e1k-buffer-overflow-poc_4.8.0-1_amd64.deb

[Changeset_67974]: https://www.virtualbox.org/changeset/67974/vbox/trunk/src/VBox/Devices/Network/DevE1000.cpp
