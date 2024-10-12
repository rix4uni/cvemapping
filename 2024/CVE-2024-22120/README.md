# Usage

```bash
python exploit.py --ip <Zabbix_IP> --sid <LowPrivileged_SID> --hostid <HostID> --phpsessid <PHPSESSID> --false_time <FalseTime> --true_time <TrueTime>
```

## Summary
This exploit was created to exploit an XXE (XML External Entity). Through it, I read the backend code of the web service and found an endpoint where I could use gopher to make internal requests on Zabbix version `6.0.27` vulnerable to Remote Code Execution.

During the reconnaissance phase, I performed a brute-force attack on the external web server to obtain the docker-compose.yml file, which provided the container name of the internal Zabbix servers. Using this information, I sent a POST request to the root of the web application via gopher and the web server returned the host-id and session id of a low-privileged user in a JSON encoded in base64 in the cookie.

With these details, I was able to adapt the original exploit to exploit a SQL Injection vulnerability in zabbix-server:10051 to obtain the administrator's session ID, and then create and execute a script to achieve remote code execution.

If you need to exploit this Zabbix vulnerability using gopher, you can modify the `InternalRequest` function to make the request in the way you need.

### What does the exploit do?
1. The script will start by attempting to extract the admin session ID using a time-based SQL injection.
2. Once the admin session ID is obtained, the script will create a reverse shell script on the Zabbix server.
3. Finally, the script will execute the reverse shell, connecting back to your machine on the specified IP and port (`10.0.46.27:5555` in the script).

### Notes:
- Make sure that your machine is listening on the specified port (`5555` in the script) to catch the reverse shell. You can use `netcat` for this:

  ```bash
  nc -lvnp 5555
  ```

- Replace the IP `10.0.46.27` and port `5555` in the `CreateScript` function with your own IP and desired port to receive the reverse shell.
