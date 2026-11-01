# 005 — NetworkPolicy Enforcement Validation

## Objective
Verify that Kubernetes NetworkPolicies block unauthorized pod-to-pod TCP connectivity to PostgreSQL and Redis while preserving the API's required dependency connectivity.

## Environment
- Cluster: Minikube
- CNI: Calico
- Test workload: BusyBox test pod
- Test pod: No `app: api` label
- Policies:
  - `default-deny-all`
  - `allow-api-to-postgres`
  - `allow-api-to-redis`
  - `allow-nginx-to-api`

## Experiment 1 — Positive Controls
Tested connectivity from the API deployment to its dependencies.

| Source | Destination | Result |
|---|---|---|
| API | PostgreSQL :5432 | ALLOW — connected |
| API | Redis :6379 | ALLOW — connected |

The API retained its required database and cache connectivity.

## Experiment 2 — Negative Controls
Deployed a temporary BusyBox test pod without the `app: api` label.

Attempted TCP connections:

| Source | Destination | Result |
|---|---|---|
| Test pod | PostgreSQL :5432 | DENY — connection timed out |
| Test pod | Redis :6379 | DENY — connection timed out |

## Observations
- The legitimate API-to-dependency connections succeeded.
- The unauthorized test pod could not establish TCP connections to PostgreSQL or Redis.
- The tests were performed in a Minikube cluster using Calico as its CNI.

## Conclusion
The positive and negative connectivity tests demonstrated that the intended application traffic remained available while the tested unauthorized TCP connections were blocked.

The results provide evidence of NetworkPolicy enforcement for the tested workloads, namespaces, destinations and ports.

These tests do not establish that every protocol, port or cluster workload is isolated. Additional policy and traffic validation would be required for broader security assurance.