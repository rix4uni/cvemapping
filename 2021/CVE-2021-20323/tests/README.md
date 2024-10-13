# How to test
A simple way to test CVE-2021-20323

## Test bug present
Start a bugged Keycloak instance (`<18.0.0`)
```bash
docker-compose -f docker-compose_kc17.yml up -d
```

Test the bug
```bash
curl -v -X POST http://localhost:8081/realms/master/clients-registrations/default -H "Content-type: application/json" -d "{\"TestFlag\":1}"
```

Expected result
```bash
< HTTP/1.1 400 Bad Request
< Referrer-Policy: no-referrer
< X-Frame-Options: SAMEORIGIN
< Strict-Transport-Security: max-age=31536000; includeSubDomains
< X-Robots-Tag: none
< X-Content-Type-Options: nosniff
< Content-Security-Policy: frame-src 'self'; frame-ancestors 'self'; object-src 'none';
< X-XSS-Protection: 1; mode=block
< Content-Type: text/html;charset=UTF-8
< content-length: 116
< 
* Connection #0 to host localhost left intact
Unrecognized field "TestFlag" (class org.keycloak.representations.idm.ClientRepresentation), not marked as ignorable
```

Cleanup containers
```bash
docker-compose -f docker-compose_kc17.yml down
```

## Test bug not present
Start a non bugged Keycloak instance (`>=18.0.0`)
```bash
docker-compose -f docker-compose_kc18.yml up -d
```

Test the bug
```bash
curl -v -X POST http://localhost:8082/realms/master/clients-registrations/default -H "Content-type: application/json" -d "{\"TestFlag\":1}"
```

Expected result
```bash
< HTTP/1.1 400 Bad Request
< Referrer-Policy: no-referrer
< X-Frame-Options: SAMEORIGIN
< Strict-Transport-Security: max-age=31536000; includeSubDomains
< X-Content-Type-Options: nosniff
< X-XSS-Protection: 1; mode=block
< Content-Type: application/json
< content-length: 1227
< 
{"error":"Unrecognized field \"TestFlag\" (class org.keycloak.representations.idm.ClientRepresentation), not marked as ignorable (43 known properties: \"enabled\", \"clientAuthenticatorType\", \"redirectUris\", \"clientId\", \"authenticationFlowBindingOverrides\", \"authorizationServicesEnabled\", \"name\", \"implicitFlowEnabled\", \"registeredNodes\", \"nodeReRegistrationTimeout\", \"publicClient\", \"attributes\", \"protocol\", \"webOrigins\", \"protocolMappers\", \"id\", \"baseUrl\", \"surrogateAuthRequired\", \"adminUrl\", \"fullScopeAllowed\", \"frontchannelLogout\", \"clientTemplate\", \"origin\", \"defaultClientScopes\", \"directGrantsOnly\", \"rootUrl\", \"secret\", \"useTemplateMappers\", \"notBefore\", \"useTemplateScope\", \"standardFlowEnabled\", \"description\", \"directAccessGrantsEnabled\", \"alwaysDisplayInConsole\", \"useTemplateConfig\", \"serviceAccountsEnabled\", \"optionalClientScopes\", \"consentRequired\", \"access\", \"bearerOnly\", \"registrationAccessToken\", \"defaultRoles\", \"auth* Connection #0 to host localhost left intact
orizationSettings\"])\n at [Source: (io.quarkus.vertx.http.runtime.VertxInputStream); line: 1, column: 14] (through reference chain: org.keycloak.representations.idm.ClientRepresentation[\"TestFlag\"])"}
```

Cleanup containers
```bash
docker-compose -f docker-compose_kc18.yml down
```