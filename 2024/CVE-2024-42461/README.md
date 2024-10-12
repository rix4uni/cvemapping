# Solución para Problemas de Verificación de Firmas ECDSA y EDDSA

## Descripción

Se han identificado problemas en la verificación de firmas ECDSA y EDDSA en el proyecto Wycheproof. Las comprobaciones ausentes durante la etapa de decodificación de firmas permiten agregar o eliminar bytes cero, lo que afecta la capacidad de envío de correos. Esta actualización en el archivo `signature.js` soluciona estos problemas al verificar la longitud de las firmas.

## Instalación

1. Clona el repositorio:
   ```sh
   git clone https://github.com/tu_usuario/tu_repositorio.git
2. Navega al directorio del proyecto:
   cd tu_repositorio
3. Instala las dependencias:
   npm install
**Uso**
1. Importa la biblioteca elliptic:
   var elliptic = require('elliptic');
   var eddsa = elliptic.eddsa;
   var ec = new elliptic.ec('secp256k1')
2. Carga la clave pública y verifica las firmas:
   var ed25519 = new eddsa('ed25519');
   var key = ed25519.keyFromPublic('7d4d0e7f6153a69b6242b522abbee685fda4420f8834b108c3bdae369ef549fa', 'hex');

// Verificación de firma EDDSA
   var msg = '54657374';
   var sig = '7c38e026f29e14aabd059a0f2db8b0cd783040609a8be684db12f82a27774ab07a9155711ecfaf7f99f277bad0c6ae7e39d4eef676573336a5c51eb6f946b30d00';
   console.log(key.verify(msg, sig));

// Verificación de firma ECDSA
   var hash = require('hash.js');
   var toArray = elliptic.utils.toArray;
   var hashMsg = hash.sha256().update(toArray(msg, 'hex')).digest();
   var pubKey = ec.keyFromPublic('04b838ff44e5bc177bf21189d0766082fc9d843226887fc9760371100b7ee20a6ff0c9d75bfba7b31a6bca1974496eeb56de357071955d83c4b1badaa0b21832e9', 'hex');
   console.log('Valid signature: ' + pubKey.verify(hashMsg, sig));



