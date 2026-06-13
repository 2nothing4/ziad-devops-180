#!/bin/bash
set -e

echo "Destroying old deployment..."
helm uninstall my-app || true
kubectl delete all --all || true
kubectl delete pvc --all || true

echo "Waiting for cleanup..."
sleep 5

echo "Deploying with Helm..."
helm install my-app ./ziad-devops-chart

echo "Waiting for pods..."
sleep 15

echo "Checking status..."
kubectl get pods

echo "Testing endpoints..."
kubectl port-forward svc/nginx 8080:80 &
sleep 3
curl localhost:8080/health
curl localhost:8080/cache

echo "Rebuild complete!"
