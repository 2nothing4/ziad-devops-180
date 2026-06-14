# Ziad DevOps 180

A production-style DevOps learning project focused on containerization, orchestration, observability, security, CI/CD, and Infrastructure as Code.

## Architecture

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


## Technologies

- **Containerization:** Docker, Docker Compose
- **Orchestration:** Kubernetes (Minikube), Helm
- **Application Stack:** Flask, PostgreSQL, Redis, Nginx
- **Observability:** Prometheus, Grafana, Alertmanager
- **Infrastructure as Code:** Terraform
- **CI/CD:** GitHub Actions
- **Security:** Kubernetes Secrets, RBAC, Network Policies

## Features

- Flask API connected to PostgreSQL
- Redis caching layer
- Nginx reverse proxy
- Multi-service Kubernetes architecture
- Multi-pod deployment with load balancing
- Persistent storage for PostgreSQL
- Health checks and self-healing
- Secret-based credential management
- Least-privilege RBAC
- Network segmentation with Network Policies
- Prometheus metrics collection
- Grafana dashboards
- Custom application metrics
- Alertmanager alert rules
- Automated CI/CD pipeline
- Helm chart linting and validation
- Terraform modules
- AWS production architecture planning

## Notable Debugging Example

**502 Bad Gateway Investigation**

- **Issue:** Nginx returned HTTP 502 responses
- **Root Cause:** Nginx configuration referenced a Kubernetes Service name that did not exist
- **Resolution:** Updated the upstream target to the correct Kubernetes Service
- **Lesson:** Kubernetes service discovery depends on exact DNS naming

## Quick Start

```bash
git clone https://github.com/2nothing4/ziad-devops-180.git
cd ziad-devops-180
helm install my-app ./ziad-devops-chart
kubectl port-forward svc/nginx 8080:80
curl localhost:8080/health
curl localhost:8080/cache

##Author
Chabane Ahmed Ziad
Aspiring DevOps / Platform Engineer
Location: Algeria
GitHub: @2nothing4
