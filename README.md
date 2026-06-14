python3 -c "
with open('/mnt/c/Users/bahat/Documents/ziad-devops-180/README.md', 'w') as f:
    f.write('''# Ziad DevOps 180 — Production Microservices Stack

**Stack:** Kubernetes, Helm, Terraform, CI/CD, Observability  
**Constraint:** No cloud access (Algeria banking) — runs locally with production patterns.

## Architecture

```mermaid
graph LR
    User -->|HTTP :80| Nginx[Nginx Reverse Proxy]
    Nginx -->|Load Balance| API[Flask API 3 Replicas]
    API -->|Read/Write| Postgres[(PostgreSQL)]
    API -->|Cache| Redis[(Redis)]
    Prometheus -->|Scrape /metrics| API
    Grafana -->|Query| Prometheus
| Layer         | Tech                              | Purpose                                        |
| ------------- | --------------------------------- | ---------------------------------------------- |
| Proxy         | Nginx                             | Single entry point, load balancing             |
| API           | Flask + Python                    | REST API with /health, /logs, /cache, /metrics |
| DB            | PostgreSQL                        | Persistent data with PVC                       |
| Cache         | Redis                             | Application caching                            |
| Orchestration | Kubernetes + Helm                 | 3 replicas, auto-healing, one-command deploy   |
| IaC           | Terraform                         | AWS production architecture (plan-validated)   |
| CI/CD         | GitHub Actions                    | Automated build, lint, validation              |
| Monitoring    | Prometheus + Grafana              | Custom metrics, latency histograms             |
| Security      | RBAC + Network Policies + Secrets | Least privilege, default-deny                  |

Quick Start
git clone https://github.com/2nothing4/ziad-devops-180.git
cd ziad-devops-180
helm install my-app ./ziad-devops-chart
kubectl port-forward svc/nginx 8080:80
curl localhost:8080/health
curl localhost:8080/cache

Contact
GitHub: @2nothing4
Location: Algeria (GMT+1, French timezone)
Target: Remote DevOps / Platform Engineer roles (EU startups)

Built through documentation-driven learning, iterative debugging, and hands-on implementation.
