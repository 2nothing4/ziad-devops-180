# 005 — NetworkPolicy Enforcement Validation

## Objective
Verify that an unauthorized test pod cannot establish TCP connections to PostgreSQL and Redis, while the API retains the required dependency connectivity.

## Environment
- Cluster: Minikube
- CNI: Calico (configured via `minikube start --cni=calico`)
- Test workload: BusyBox test pod
- Policies: `default-deny-all`, `allow-api-to-postgres`, `allow-api-to-redis`, `allow-nginx-to-api`

## Experiment

### 1. Positive Control (API Connectivity)
- **API -> PostgreSQL:** Connection successful.
- **API -> Redis:** Connection successful.
*Conclusion:* The API is healthy and the NetworkPolicy correctly permits required traffic.

### 2. Negative Control (Unauthorized Pod)
- Deployed an unprivileged `busybox` pod without the `app: api` label.
- Attempted PostgreSQL TCP connection on port 5432: **Connection timed out.**
- Attempted Redis TCP connection on port 6379: **Connection timed out.**

## Conclusion
The NetworkPolicies are actively enforced by the Calico CNI. Unauthorized pods cannot establish TCP connections to the database or cache, proving that the principle of least privilege is successfully applied to network traffic.