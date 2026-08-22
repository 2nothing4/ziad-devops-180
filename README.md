## Helm Chart

Deploy the entire stack with one command:

```bash
helm install ziad-devops ./helm/ziad-devops ![Deploy to Render](https://github.com/2nothing4/ziad-devops-180/actions/workflows/render-deploy.yml/badge.svg)
# Ziad DevOps 180

A production-style DevOps learning project focused on containerization, orchestration, observability, security, CI/CD, and Infrastructure as Code.

The goal of this repository is to document the practical implementation of a complete application platform using modern DevOps tooling and workflows.

> **New here? Start with the [debugging incidents](docs/day29-loki-promtail-debug.md) — they show how this platform was built, broken, and fixed.**

---

## Architecture

```text
                    +-------------+
                    |    Nginx    |
                    +------+------+
                           |
                           v
                +----------+----------+
                | Flask API (3 Pods)  |
                +----------+----------+
                           |
              +------------+------------+
              |                         |
              v                         v
        +-----------+             +-----------+
        | PostgreSQL|             |   Redis   |
        +-----------+             +-----------+
              ^
              |
      +------------------+
      | Prometheus       |
      | Loki             |
      | Grafana          |
      | Promtail         |
      | Alertmanager     |
      +------------------+
```

---
---

## 🚀 Live Deployment

**Flask API deployed on Render (cloud):** https://ziad-flask-app.onrender.com

| Endpoint | Description | Status |
|----------|-------------|--------|
| `/` | Service status | ✅ Live |
| `/health` | PostgreSQL health check | ✅ Live |
| `/logs` | Database query results | ✅ Live |
| `/cache` | Redis cache test | ✅ Live |
| `/metrics` | Prometheus
Loki metrics | ✅ Live |

**Tech stack on Render:**
- Flask + Gunicorn
- PostgreSQL (managed)
- Redis (managed)
- Environment variables for configuration
- Auto-deploy from GitHub

---

## Local vs Cloud Architecture

```text
   LOCAL (Minikube)                    CLOUD (Render)
   ┌─────────────┐                    ┌─────────────┐
   │    Nginx    │                    │  Render LB  │
   └──────┬──────┘                    └──────┬──────┘
          │                                  │
          v                                  v
   ┌──────────────┐                  ┌────────────────┐
   │Flask (3 Pods)│                  │Flask (Gunicorn)│
   └──────┬───────┘                  └───────┬────────┘
          │                                  │
     ┌────┴────┐                         ┌───┴───┐
     │         │                         │       │
     v         v                         v       v
┌────────┐ ┌───────┐              ┌─────────┐ ┌─────────┐
│Postgres│ │Redis  │              │Postgres │ │Redis    │
│(local) │ │(local)│              │(managed)│ │(managed)│
└────────┘ └───────┘              └─────────┘ └─────────┘
```
## Technologies

### Containerization

* Docker
* Docker Compose

### Orchestration

* Kubernetes (Minikube)
* Helm

### Application Stack

* Flask
* PostgreSQL
* Redis
* Nginx

### Observability

- **Prometheus** — metrics collection
- **Loki** — log aggregation
- **Grafana** — dashboards and visualization
- **Promtail** — log shipping
- **Alertmanager** — alert routing and notifications

### Infrastructure as Code

* Terraform

### CI/CD

* GitHub Actions

### Security

* Kubernetes Secrets
* RBAC
* Network Policies

---

## Features

### Application Platform

* Flask API connected to PostgreSQL
* Redis caching layer
* Nginx reverse proxy
* Multi-service architecture

### Kubernetes

* Multi-pod deployment
* Service discovery
* Load balancing
* Persistent storage
* Health checks
* Resource management

### Security

* Secret-based credential management
* Least-privilege RBAC configuration
* Network segmentation using Kubernetes Network Policies
* Trivy + Checkov security scanning

### Observability

* Prometheus
Loki metrics collection
* Grafana
Promtail dashboards
* Custom application metrics
* Alertmanager alert rules
* Alertmanager webhook alerts (end-to-end tested)
* In-cluster alert receiver deployment

### CI/CD

* Automated GitHub Actions workflow
* Docker image validation
* Helm chart linting
* Manifest rendering validation

### Infrastructure as Code

* Terraform modules
* Reusable infrastructure definitions
* AWS production architecture planning

---

## Notable Debugging Example

### 502 Bad Gateway Investigation

Issue:

* Nginx returned HTTP 502 responses.

Root Cause:

* Nginx configuration referenced a Kubernetes Service name that did not exist.

Resolution:

* Updated the upstream target to the correct Kubernetes Service.
* Redeployed configuration using Kubernetes manifests.

Lesson:

* Kubernetes service discovery depends on exact DNS naming and service registration.

### Alertmanager Webhook Networking

**Issue:** Alertmanager could not reach the webhook receiver running on the WSL2 host.  
**Root Cause:** `host.minikube.internal` resolved to the wrong network interface.  
**Resolution:** Deployed the alert receiver as an in-cluster pod with a Kubernetes Service. Alertmanager now routes via cluster DNS.  
**Lesson:** In-cluster services should communicate via cluster DNS, not host networking.

---

## Production-Oriented Enhancements

* Helm-based deployments
* Persistent PostgreSQL storage
* Resource requests and limits
* Custom Prometheus
Loki metrics
* Alerting rules
* Infrastructure modularization
* Security hardening with RBAC and Network Policies

---

## Current Status

| Area | Local | Cloud |
|------|-------|-------|
| Docker | ✅ | - |
| Docker Compose | ✅ | - |
| Kubernetes (Minikube) | ✅ | - |
| Helm | ✅ | - |
| Terraform | ✅ | - |
| CI/CD (GitHub Actions) | ✅ | - |
| Monitoring (Prometheus + Grafana + Loki + Promtail + Alertmanager) | ✅ | - |
| Security Scanning (Trivy/Checkov) | ✅ | - |
| **Cloud Deployment (Render)** | - | **✅** |
| **Live URL for Portfolio** | - | **✅** |

Repository continues to evolve as new capabilities are implemented and documented.

## Testing

- `pytest` suite with CI/CD integration via GitHub Actions
- Tests cover `/health`, `/cache`, and `/metrics` endpoints
- Database connections mocked for containerized test environments
- See [commit history](https://github.com/2nothing4/ziad-devops-180/commits/main) for iterative debugging process
