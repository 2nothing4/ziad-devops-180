# NetworkPolicy Regression Tests

## Objective
Automate connectivity checks for the isolated Kubernetes network-policy test environment.

## Environment
- Kubernetes: Minikube
- CNI: Calico
- Test namespace: net-test
- Test workload: test-pod
- PostgreSQL namespace: default

## Usage
Run from the repository root:
```bash
bash ./test-network.sh