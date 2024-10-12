# CVE-2022-27518_POC

```bash
docker pull quay.io/citrix/citrix-k8s-cpx-ingress:13.0-58.30
```
Use the following command to verify if CPX image is installed in docker images
```bash
docker images | grep 'citrix-k8s-cpx-ingress'
```
Use the following command to create a CPX container instance running in bridge mode
```bash
docker run --rm -dt -P --privileged=true -e EULA=yes --ulimit core=-1 --name cpx-hello-world quay.io/citrix/citrix-k8s-cpx-ingress:13.0-58.30 
```
Once CPX container is deployed successfully, the following command can be used to access the Shell of CPX container
```bash
docker exec -it cpx-hello-world bash
```