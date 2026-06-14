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

Completed areas:

* Docker
* Docker Compose
* Linux fundamentals
* GitHub Actions
* Kubernetes
* Helm
* Terraform
* Monitoring
* Logging & Metrics
* Security Hardening
* Infrastructure as Code

Repository continues to evolve as new capabilities are implemented and documented.

---

## Author

**Chabane Ahmed Ziad**

Aspiring DevOps / Platform Engineer

Location: Algeria

GitHub: @2nothing4
