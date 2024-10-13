# CVE-2018-18925
Exploitation of CVE-2018-18925 a Remote Code Execution against the Git self hosted tool: [Gogs](https://gogs.io/).

Gogs is based on the `Macaron` framework. The system used to manage session is very similar to what PHP does. The session identifier in the cookie is mapped to a file on the file system. When the web server receives a request with a session identifier (as a cookie), it looks up for the file on the file system.

The vulnerability is a simple directory traversal when retrieving the file used for the session on the file system. You can for example, set the `i_like_gogits` cookie to `../../../../../../etc/passwd` to get an error from the server.

![image](https://user-images.githubusercontent.com/48088579/133288053-82c28b18-5e8f-439c-8de7-ed555eb1899c.png)

## Exploitation:
In order to exploit the session bypass, we will need a way to upload a specially crafted file, then we will use this file as our session id, we can create our own crafted session id file with https://github.com/RyouYoo/CVE-2018-18925/blob/main/main.go.

### Usage:
```bash
go run main.go
```

### Uploading the malicious file and logged in as administrator

When creating the copy of the repository locally, Gogs put the files in /data/gogs/data/tmp/local-repo/[REPO_ID]/[FILENAME] (this repository is only created when you use the "Upload file" functionality). 

![image](https://user-images.githubusercontent.com/48088579/133289129-48d06236-e651-400f-aad7-db5b147e0ea7.png)


Where [FILENAME] is the name of the file you upload and [REPO_ID] is the repository identifier that can be found using the `Fork` link:

![image](https://user-images.githubusercontent.com/48088579/133288862-d89cde85-e276-49c1-bae1-497f607f58e5.png)

Where `5` is the repo id.

By default, the sessions are stored in `/data/gogs/data/sessions/`. Therefore, you can use the following relative path for your session id: ``../tmp/local-repo/[REPO_ID]/[FILENAME]``. By using this path in your `i_like_gogits` cookie, you should be logged in as `administrator`.

![133289399-47f6692b-7cfa-443d-89d3-caa5b9828250](https://user-images.githubusercontent.com/48088579/133319388-5cd8ae70-40b5-4de6-95cd-5fb14ca67d4e.png)

# Remote Code Execution:

In order to get RCE, you can use the git hooks functionality in a given repository to run a shell script.

![image](https://user-images.githubusercontent.com/48088579/133289770-f08bfe44-d0c1-4aa4-a184-15cfecb2465c.png)

In `pre-receive` inject your code:

![image](https://user-images.githubusercontent.com/48088579/133289883-cff3302c-0cda-4a5e-8485-7169d8cc4236.png)

Then make a push request, with git or with create file function to get the hook executed.
