# SnakeYAML-CVE-2022-1471-POC
Code for veracode blog

To demonstrate the Code Execution, 
1. Build the project using maven 
2. Execute `python3 -m http.server 8080` to run the http server
3. Run `exploit.java`. You should observe a HTTP GET request on the server
4. To demonstrate how SnakeYAML 2.0 prevents the attack, comment out the 1.33 dependency in the `pom.xml`
5. Uncomment the 2.0 dependency, then rebuild the project, 
6. Comment out `exploit.java` and uncomment `Poc.java`
7. Run `Poc.java` and observe no GET request
