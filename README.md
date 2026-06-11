\# Ziad - DevOps 180



\*\*Started:\*\* 2026-06-09

\*\*Rule:\*\* No switching. No new fields. No more AI opinions.



\## Day 1 - COMPLETE

\- \[x] Check Python version: Python 3.14.5

\- \[x] First commit pushed



\## Day 2 - COMPLETE

\- \[x] Python script fetches GitHub API

\- \[x] repo\_info.json created and pushed



\## Day 3 - COMPLETE

\- \[x] WSL installed

\- \[x] Ubuntu terminal working

\- \[x] First Linux commands executed

\- \[x] Created first Linux file: day3-linux.txt



\## Day 4 - COMPLETE

\- \[x] Docker Desktop installed

\- \[x] First container ran

\- \[x] Built custom Dockerfile

\- \[x] Containerized Python script



\## Day 5 - COMPLETE

\- \[x] Docker Compose installed

\- \[x] Multi-container system running

\- \[x] Python + PostgreSQL connected



\## Day 6 - COMPLETE

\- \[x] GitHub Actions workflow created

\- \[x] Automated Docker build on every push

\- \[x] CI/CD pipeline running with GREEN CHECKMARK

\- \[x] Multi-container PostgreSQL + Python test automated



\## Day 7 - COMPLETE

\- \[x] Kubernetes cluster running locally (Minikube)

\- \[x] PostgreSQL deployed to Kubernetes

\- \[x] Python app deployed to Kubernetes

\- \[x] App connects to database inside cluster

\- \[x] Fixed psycopg2 dependency and timing issues

\- \[x] Kubernetes manifests stored in repo

\- \[x] Multi-container orchestration working end-to-end



\## Day 8 - COMPLETE

\- \[x] Terraform installed

\- \[x] First Infrastructure as Code file created

\- \[x] Nginx web server deployed with code

\- \[x] Server destroyed cleanly with code



\## Day 9 - COMPLETE

\- \[x] Flask web application built

\- \[x] Python API connects to PostgreSQL database

\- \[x] Docker image built and loaded into Minikube

\- \[x] Deployed to Kubernetes with service

\- \[x] Application accessible in browser via port-forward

\- \[x] Real web API serving database content

\- \[x] / endpoint: welcome message

\- \[x] /logs endpoint: database query returning JSON



\## Day 10 - COMPLETE

\- \[x] Added /health endpoint to Flask app

\- \[x] Health check verifies database connection

\- \[x] Kubernetes livenessProbe configured

\- \[x] Kubernetes readinessProbe configured

\- \[x] Application version bumped to Day 10

\- \[x] Health endpoint returns: {"database": "connected", "status": "healthy"}



\## Day 11 - COMPLETE

\- \[x] Prometheus deployed to Kubernetes

\- \[x] Prometheus scraping Flask app health endpoint

\- \[x] Grafana deployed to Kubernetes

\- \[x] Grafana dashboard created showing app health (up=1)

\- \[x] Monitoring stack: Prometheus + Grafana + Flask app

\- \[x] Real-time visualization of application uptime



\## Day 12 - COMPLETE

\- \[x] Nginx reverse proxy deployed to Kubernetes

\- \[x] Nginx routes traffic from port 80 to Flask service

\- \[x] Production-grade architecture: Nginx → Flask → PostgreSQL

\- \[x] All three layers accessible through single entry point



\## Day 13 - COMPLETE

\- \[x] Flask app scaled to 3 replicas

\- \[x] Load balancing across multiple pods

\- \[x] Nginx distributing traffic to 3 Flask instances



\## Day 14 - COMPLETE

\- \[x] Redis cache deployed to Kubernetes

\- \[x] Caching layer added to architecture

\- \[x] Core DevOps stack COMPLETE: 14 milestones



## Day 15 - COMPLETE

- [x] Helm chart created: `ziad-devops-chart/`

- [x] One command deploys full stack: `helm install my-app ./ziad-devops-chart`

- [x] Stack includes: Nginx, Flask API (3 replicas), PostgreSQL, Redis, Prometheus, Grafana

- [x] Tested: `curl localhost:8080/cache` returns Redis cache data

- [x] Day 15: Helm orchestration COMPLETE
