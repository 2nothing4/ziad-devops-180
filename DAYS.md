# Engineering Progress Log

## Day 37 — Configuration Drift (Helm)

- **Objective:** Consolidate Helm charts into one source of truth.
- **Changes:** Moved `ziad-devops-chart` to `helm/ziad-devops`, fixed CI paths, updated `rebuild.sh`.
- **Validation:** Green CI pipeline.

## Day 38 — Automated Cache Testing

- **Objective:** Add automated tests for the `/cache` endpoint, covering Redis success and failure paths.
- **Changes:** Added mocked Redis tests in `tests/test_app.py`, including `test_cache_endpoint_success` and `test_cache_endpoint_redis_failure`.
- **Validation:** Four pytest tests passed locally and in CI.

## Day 39 — Application Hardening

- **Objective:** Prevent API information leakage.
- **Changes:** Replaced raw Python exception strings with generic JSON error messages for `/health`, `/logs`, and `/cache`. Added basic server-side error output.
- **Validation:** Four pytest tests passed. CI green.

## Day 40 — Cloud Sandboxing and CI/CD

- **Objective:** Resolve deployment failures following repository dependency restructuring.
- **Changes:** Updated Docker to use the repository root as its build context. Added a nested `day9-flask/requirements.txt` compatibility include referencing the root requirements file. Updated the Render deployment workflow's curl request to follow redirects.
- **Validation:** All four GitHub Actions workflows reported green.

## Day 41 — Application Lifecycle

- **Objective:** Remove import-time database initialization.
- **Changes:** Removed the top-level `init_db()` call from `app.py`. Created `manage_db.py` for explicit initialization. Updated exception handling so initialization failures propagate rather than being reported as successful. Added a test for import side effects.
- **Validation:** Five pytest tests passed. CI green.

## Day 42 — Kubernetes Health Probes

- **Objective:** Separate process liveness from dependency readiness.
- **Changes:** Added `/livez` for process health and `/readyz` for PostgreSQL readiness. Configured Kubernetes `livenessProbe` and `readinessProbe` in the canonical Helm chart. Added tests for the new endpoint behavior.
- **Validation:** Nine pytest tests passed locally. GitHub Actions reported green.

## Day 43 — PostgreSQL Failure and Recovery

- **Objective:** Verify that Kubernetes handles database outages and recovery without unnecessarily restarting healthy API containers.
- **Changes:** Scaled PostgreSQL down to zero replicas. Observed API pods transition to `NotReady` while `/livez` continued returning HTTP 200 and `/readyz` returned HTTP 503. Restored PostgreSQL and observed API readiness recover.
- **Validation:** API container restart counts reportedly remained unchanged. Recovery documented in `docs/incidents/004-postgresql-outage-recovery.md`. Nginx experienced separate restarts that require investigation.

## Day 44 — Kubernetes Container Security Contexts

- **Objective:** Harden the Flask API container through least-privilege execution.
- **Changes:**
  - Created dedicated `appuser` and `appgroup` identities (UID/GID 10001).
  - Configured the Dockerfile `USER` instruction.
  - Enabled Kubernetes `runAsNonRoot`.
  - Set explicit `runAsUser` and `runAsGroup`.
  - Disabled privilege escalation.
  - Dropped all Linux capabilities.
  - Applied the `RuntimeDefault` seccomp profile.
- **Validation:**
  - Verified the runtime identity using `kubectl exec ... id`.
  - Confirmed UID 10001 and GID 10001.
  - Verified the updated ReplicaSet replaced the previous pods.
  - Confirmed application health probes remained healthy.

## Day 45 — Read-Only Root Filesystem

- **Objective:** Reduce runtime filesystem modification by making the container root filesystem read-only.
- **Changes:**
  - Enabled `readOnlyRootFilesystem: true` in the API container security context.
  - Added `emptyDir` volumes for `/tmp` and `/app/__pycache__` to provide explicitly writable temporary paths.
- **Validation:**
  - Confirmed writing `/app/hacked.txt` failed with `Read-only file system`.
  - Confirmed writing `/tmp/test.txt` succeeded.
  - Checked application logs for successful `/livez` and `/readyz` requests.
  - Confirmed the new API pods reportedly had zero restarts.

## Day 46 — NetworkPolicy Enforcement

- **Objective:** Verify that Kubernetes NetworkPolicies actively restrict unauthorized pod-to-pod traffic.
- **Changes:**
  - Configured the Minikube environment with Calico CNI.
  - Tested API-to-PostgreSQL and API-to-Redis connectivity.
  - Deployed a temporary BusyBox test pod without the API workload label.
  - Tested unauthorized TCP connections to PostgreSQL and Redis.
- **Validation:**
  - API → PostgreSQL: Connected.
  - API → Redis: Connected.
  - Test pod → PostgreSQL: Connection timed out.
  - Test pod → Redis: Connection timed out.
  - Results documented in `docs/incidents/005-network-policy-enforcement.md`.

  ## Day 47 — Security Verification
- **Objective:** Audit the security controls implemented across Days 44-46.
- **Results:** See `docs/security-audit/day47/`.
# Day 47: Secrets Management Audit

## Audit C — Kubernetes Secrets and Credential Management

### Finding 1: Plaintext Credentials in Git
- **Control:** No plaintext secrets in Helm templates.
- **Expected:** Secrets should be injected securely (e.g., via external secrets or securely generated at deploy time).
- **Observed:** `helm/ziad-devops/templates/secret.yaml` contains `password: secret123` in `stringData`.
- **Evidence:** `Get-Content helm/ziad-devops/templates/secret.yaml`
- **Status:** **CRITICAL GAP**
- **Remaining Risk:** Anyone with read access to the GitHub repository can read the database password. If this was a real production database, it would be compromised.

### Finding 2: Git History Hygiene
- **Control:** No tracked `.terraform` provider binaries or plan files.
- **Expected:** Clean repository without bulky binaries or sensitive plan files.
- **Observed:** `.terraform/` and `plan.txt` were tracked but have now been untracked via `git rm --cached`.
- **Status:** PASS (Remediated during audit)

## Day 48 — Secrets Remediation
- **Objective:** Remove hardcoded database credentials from application and deployment configuration.
- **Changes:** Removed fallback password from `app.py`. Moved password to a Kubernetes Secret. Updated workloads to consume the secret.
- **Validation:** API successfully connected to PostgreSQL. Verified no plaintext credentials remained in tracked files.

## Day 49 — RBAC & Service Account Hardening
- **Objective:** Reduce unnecessary Kubernetes API access for the application.
- **Changes:** Disabled `automountServiceAccountToken` in the Deployment. Deleted unnecessary `api-role` and `api-binding` from the Helm chart and cluster.
- **Validation:** Verified the token is no longer mounted in the API pod. Verified the ServiceAccount can no longer list pods (`kubectl auth can-i` returns `no`).