# Day 29: Loki + Promtail Troubleshooting Log

## Stack
- Loki 2.9.0
- Promtail 2.9.0 (root user)
- Minikube (Docker driver)

## Problem
Promtail running but no logs in Grafana. Targets endpoint empty.

## Root Causes & Fixes

### 1. Path mismatch
Actual path: `/var/log/pods/<namespace>_<pod>_<uid>/<container>/<restart>.log`
Wrong glob: `/var/log/pods/*/*/*/*.log` (4 levels)
Fixed glob: `/var/log/pods/*/*/*.log` (3 levels)

### 2. Permissions
Log dirs owned by root `drwxr-x---`. Promtail non-root = no access.
Fix: `securityContext: runAsUser: 0` in deployment.

## Key Commands
kubectl exec -it deployment/promtail -- sh -c "find /var/log/pods -name '*.log' | head -5"
kubectl exec -it deployment/promtail -- sh -c "ls -la /var/log/pods/ | head -5"
curl -s http://localhost:9080/ready

## Verification
Grafana Explore → Loki → {job="kubernetes-pods"} → logs flowing
