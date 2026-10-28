# Ziad DevOps 180 🚀

[![Deploy to Render](https://github.com/2nothing4/ziad-devops-180/actions/workflows/render-deploy.yml/badge.svg)](https://github.com/2nothing4/ziad-devops-180/actions/workflows/render-deploy.yml)

A production-style DevOps learning project focused on containerization, orchestration, observability, security, CI/CD, and Infrastructure as Code.

> **New here? Start with the [debugging incidents](docs/day29-loki-promtail-debug.md)** — they show how this platform was built, broken, and fixed.

## 📑 Table of Contents
- [🚀 Live Deployment](#-live-deployment)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Tech Stack](#️-tech-stack)
- [✨ Key Features](#-key-features)
- [🐛 Notable Debugging Examples](#-notable-debugging-examples)
- [📊 Project Status](#-project-status)

---

## 🚀 Live Deployment

**Flask API deployed on Render (cloud):** [https://ziad-flask-app.onrender.com](https://ziad-flask-app.onrender.com)
*(Note: Hosted on Render free tier, may take ~50s to cold start).*

| Endpoint | Description | Status |
|----------|-------------|--------|
| `/` | Service status | ✅ Live |
| `/health` | PostgreSQL health check | ✅ Live |
| `/logs` | Database query results | ✅ Live |
| `/cache` | Redis cache test | ✅ Live |
| `/metrics` | Prometheus metrics | ✅ Live |

---

## 🏗️ Architecture

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
### Local vs Cloud Architecture
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
## 🛠️ Tech Stack

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white)

✨ Key Features
☁️ Infrastructure as Code: Terraform modules for AWS production architecture planning.

📦 Containerization: Docker & Docker Compose for local development.

☸️ Orchestration: Kubernetes (Minikube) with Helm for multi-pod deployments and persistent storage.

📊 Observability: Full stack monitoring with Prometheus, Grafana, Loki, and Promtail. End-to-end tested Alertmanager webhooks.

🔒 Security: Least-privilege RBAC, Network Policies, Kubernetes Secrets, and automated Trivy/Checkov scanning.

🔄 CI/CD: Automated GitHub Actions workflows for Docker image validation, Helm linting, and manifest rendering.

🐛 Notable Debugging Examples
1. 502 Bad Gateway Investigation
Issue: Nginx returned HTTP 502 responses.

Root Cause: Nginx configuration referenced a Kubernetes Service name that did not exist.

Resolution: Updated the upstream target to the correct Kubernetes Service and redeployed.

Lesson: Kubernetes service discovery depends on exact DNS naming and service registration.

2. Alertmanager Webhook Networking
Issue: Alertmanager could not reach the webhook receiver running on the WSL2 host.

Root Cause: host.minikube.internal resolved to the wrong network interface.

Resolution: Deployed the alert receiver as an in-cluster pod with a Kubernetes Service. Alertmanager now routes via cluster DNS.

Lesson: In-cluster services should communicate via cluster DNS, not host networking.

## 📊 Project Status

| Area | Local | Cloud |
|------|:-----:|:-----:|
| Docker & Docker Compose | ✅ | - |
| Kubernetes (Minikube) & Helm | ✅ | - |
| Terraform (IaC) | ✅ | - |
| CI/CD (GitHub Actions) | ✅ | - |
| Monitoring Stack (Prometheus, Grafana, Loki, Alertmanager) | ✅ | - |
| Security Scanning (Trivy/Checkov) | ✅ | - |
| **Cloud Deployment (Render)** | - | **✅** |
| **Live URL for Portfolio** | - | **✅** |

🧪 Testing
pytest suite with CI/CD integration via GitHub Actions.

Tests cover /health, /cache, and /metrics endpoints.

Database connections mocked for containerized test environments.
