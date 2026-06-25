# Ziad DevOps 180

A production-style DevOps learning project focused on containerization, orchestration, observability, security, CI/CD, and Infrastructure as Code.

The goal of this repository is to document the practical implementation of a complete application platform using modern DevOps tooling and workflows.

---

## Architecture

```text
                    +-------------+
                    |    Nginx    |
                    +------+------+
                           |
                           v
                +----------+----------+
                | Flask API (3 Pods) |
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
      | Grafana          |
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
| `/metrics` | Prometheus metrics | ✅ Live |

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
│   Nginx     │                    │  Render LB   │
└──────┬──────┘                    └──────┬──────┘
       │                                │
       v                                v
┌──────────────┐                  ┌──────────────┐
│ Flask (3 Pods)│                  │ Flask (Gunicorn)│
└──────┬───────┘                  └──────┬───────┘
       │                                │
   ┌───┴───┐                        ┌───┴───┐
   │       │                        │       │
   v       v                        v       v
┌──────┐ ┌──────┐              ┌──────┐ ┌──────┐
│ Postgres│ │ Redis │              │ Postgres│ │ Redis │
│ (local)│ │(local)│              │(managed)│ │(managed)│
└──────┘ └──────┘              └──────┘ └──────┘
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

* Prometheus
* Grafana
* Alertmanager

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

### Observability

* Prometheus metrics collection
* Grafana dashboards
* Custom application metrics
* Alertmanager alert rules

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

---

## Production-Oriented Enhancements

* Helm-based deployments
* Persistent PostgreSQL storage
* Resource requests and limits
* Custom Prometheus metrics
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
| Monitoring (Prometheus/Grafana) | ✅ | - |
| **Cloud Deployment (Render)** | - | **✅** |
| **Live URL for Portfolio** | - | **✅** |

Repository continues to evolve as new capabilities are implemented and documented.

---

## Author

**Chabane Ahmed Ziad**

Aspiring DevOps / Platform Engineer

Location: Algeria

GitHub: @2nothing4
# auto-deploy test Thu Jun 25 15:15:34 CET 2026
