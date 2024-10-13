# ENGLISH
# Description 

This application allows you to replace a value in a JSON Web Token (JWT) using the HMAC-SHA256 method to recalculate the signature. It takes as input a token, a key to replace, and the new value associated with that key.
---

# Usage
Clone or download the application's source code.
```shell
git clone https://github.com/WinDyAlphA/CVE-2015-9235_JWT_key_confusion
cd CVE-2015-9235_JWT_key_confusion
```

The file token.txt contains a valid JWT token as an example. You can modify it or replace it with your own token.

Run the application using the command line with the appropriate arguments:
```shell
python main.py -t token_path -k key_to_replace -v new_value
```
-t or --token: The path to the file containing the original JWT token.

-k or --key: The key to be replaced in the token.

-v or --value: The new value to be associated with the key.

The application will display the new JWT token with the updated key.

# Example of Use
```shell
python main.py -t token.txt -k user -v "thierry23' and 1=1-- -"
```
# CVE 2015-9235 Vulnerability
This application was built to illustrate a known security vulnerability referenced as CVE-2015-9235.

# Vulnerability Description
In the jsonwebtoken module for Node.js before version 4.2.2, it is possible for an attacker to bypass verification when a token is signed with an asymmetric key (RS/ES family) of algorithms, but instead, the attacker sends a token signed with a symmetric algorithm (HS* family).

<br>

---  

<br>



# FRENCH
# Description
Cette application permet de remplacer une valeur dans un jeton JWT (JSON Web Token) en utilisant la méthode HMAC-SHA256 pour recalculer la signature. Elle prend en entrée un jeton, une clé à remplacer et la nouvelle valeur associée à cette clé.
---  



# Utilisation

Clonez ou téléchargez le code source de l'application.
```shell
git clone https://github.com/WinDyAlphA/CVE-2015-9235_JWT_key_confusion
cd CVE-2015-9235_JWT_key_confusion
```

Le fichier token.txt contient un jeton JWT valide en tant qu'exemple. Vous pouvez le modifier ou le remplacer par votre propre jeton.

Exécutez l'application en utilisant la ligne de commande avec les arguments appropriés :

``` shell
python main.py -t chemin_du_jeton -k clé_à_remplacer -v nouvelle_valeur
```
-t ou --token : Le chemin du fichier contenant le jeton JWT d'origine.

-k ou --key : La clé à remplacer dans le jeton.

-v ou --value : La nouvelle valeur à associer à la clé.

L'application affichera le nouveau jeton JWT avec la clé mise à jour.

# Exemple d'utilisation
```shell
python main.py -t token.txt -k utilisateur -v "thierry23' and 1=1-- -"
```

# Vulnérabilité CVE 2015-9235
Cette application a été construite pour illustrer une vulnérabilité de sécurité connue sous la référence CVE-2015-9235.

# Description de la Vulnérabilité
Dans le module jsonwebtoken pour Node.js avant la version 4.2.2, il est possible pour un attaquant de contourner la vérification lorsqu'un jeton est signé numériquement avec une clé asymétrique (famille RS/ES) d'algorithmes, mais à la place, l'attaquant envoie un jeton signé numériquement avec un algorithme symétrique (famille HS*).
