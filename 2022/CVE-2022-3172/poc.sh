kubectl apply -f attacker-deployment.yaml
kubectl apply -f attacker-service.yaml
kubectl apply -f attack-apiservice.yaml

kubectl wait --for=condition=available --timeout=5m deployment/attacker-deployment
kubectl wait --for=condition=available --timeout=5m service/attacker-service
kubectl wait --for=condition=established --timeout=5m apiservice/attack-apiservice
