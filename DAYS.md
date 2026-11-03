# Engineering Progress Log — Ziad DevOps 180

> **Coverage in this document:** Days 37–49. This file preserves the supplied engineering log and records the reported Day 48–49 remediations. Earlier entries (Days 1–36) were not included in the source material used to prepare this version; merge them from your existing `DAYS.md` before replacing it if you want the complete 180-day history in one file.
>
> **Evidence standard:** “Validation” below records the results reported during the work. Keep command output, screenshots, workflow runs and incident reports in the repository where available. A configuration change is not proof of runtime behavior by itself.

---

## Day 37 — Configuration Drift (Helm)

- **Objective:** Consolidate Helm charts into one source of truth.
- **Changes:**
  - Moved `ziad-devops-chart` to `helm/ziad-devops`.
  - Fixed CI paths to use the canonical chart location.
  - Updated `rebuild.sh` to use the canonical chart.
- **Validation:** Green CI pipeline.

## Day 38 — Automated Cache Testing

- **Objective:** Add automated tests for the `/cache` endpoint, covering Redis success and failure paths.
- **Changes:**
  - Added mocked Redis tests in `tests/test_app.py`.
  - Added `test_cache_endpoint_success`.
  - Added `test_cache_endpoint_redis_failure`.
- **Validation:** Four pytest tests passed locally and in CI.

## Day 39 — Application Hardening

- **Objective:** Prevent API information leakage.
- **Changes:**
  - Replaced raw Python exception strings with generic JSON error messages for `/health`, `/logs` and `/cache`.
  - Added basic server-side error output.
- **Validation:** Four pytest tests passed. CI was green.

## Day 40 — Cloud Sandboxing and CI/CD

- **Objective:** Resolve deployment failures following repository dependency restructuring.
- **Changes:**
  - Updated Docker to use the repository root as its build context.
  - Added a nested `day9-flask/requirements.txt` compatibility include referencing the root requirements file.
  - Updated the Render deployment workflow's `curl` request to follow redirects.
- **Validation:** All four GitHub Actions workflows reported green.

## Day 41 — Application Lifecycle

- **Objective:** Remove import-time database initialization.
- **Changes:**
  - Removed the top-level `init_db()` call from `app.py`.
  - Created `manage_db.py` for explicit database initialization.
  - Updated exception handling so initialization failures propagate rather than being reported as successful.
  - Added a test for import side effects.
- **Validation:** Five pytest tests passed. CI was green.

## Day 42 — Kubernetes Health Probes

- **Objective:** Separate process liveness from dependency readiness.
- **Changes:**
  - Added `/livez` for process health.
  - Added `/readyz` for PostgreSQL readiness.
  - Configured Kubernetes `livenessProbe` and `readinessProbe` in the canonical Helm chart.
  - Added tests for the new endpoint behavior.
- **Validation:** Nine pytest tests passed locally. GitHub Actions reported green.

## Day 43 — PostgreSQL Failure and Recovery

- **Objective:** Verify that Kubernetes handles database outages and recovery without unnecessarily restarting healthy API containers.
- **Changes and experiment:**
  - Scaled PostgreSQL down to zero replicas.
  - Observed API pods transition to `NotReady`.
  - Observed `/livez` continue returning HTTP 200 while `/readyz` returned HTTP 503.
  - Restored PostgreSQL and observed API readiness recover.
- **Validation:**
  - API container restart counts reportedly remained unchanged during the experiment.
  - Recovery was documented in `docs/incidents/004-postgresql-outage-recovery.md`.
  - Nginx experienced separate restarts that were not explained by this experiment and remain an investigation item.

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
  - API → PostgreSQL (5432): Connected.
  - API → Redis (6379): Connected.
  - Test pod → PostgreSQL (5432): Connection timed out.
  - Test pod → Redis (6379): Connection timed out.
  - Results were documented in `docs/incidents/005-network-policy-enforcement.md`.

## Day 47 — Security Verification

- **Objective:** Audit the security controls implemented across Days 44–46.
- **Results:** Detailed evidence is recorded in `docs/security-audit/day47/`.

### Audit A — Container Identity

- **Control:** Run the application container as a non-root user with reduced Linux capabilities.
- **Observed:** The API process ran with UID/GID 10001; the capability set was reported as empty (`CapEff: 0000000000000000`).
- **Status:** PASS.

### Audit B — Filesystem Restrictions

- **Control:** Prevent writes to the container root filesystem while preserving required temporary write paths.
- **Observed:** The root filesystem was read-only; `/tmp` remained writable through its dedicated `emptyDir` mount.
- **Status:** PASS.

### Audit C — Kubernetes Secrets and Credential Management

#### Finding 1 — Plaintext Credentials in Git

- **Control:** No plaintext secrets in Helm templates.
- **Expected:** Secrets should be injected securely, for example through an external secrets system or a securely generated deployment-time Secret.
- **Observed:** `helm/ziad-devops/templates/secret.yaml` contained `password: secret123` in `stringData`.
- **Evidence command:** `Get-Content helm/ziad-devops/templates/secret.yaml`
- **Status:** CRITICAL GAP at the time of the audit.
- **Risk:** Anyone with read access to the repository could read the database password. If the credential had been used for a real production database, it would have required rotation.

#### Finding 2 — Git History Hygiene

- **Control:** No tracked `.terraform` provider binaries or generated plan files.
- **Expected:** The repository should not track bulky provider binaries or generated plan artifacts that may contain sensitive information.
- **Observed:** `.terraform/` and `plan.txt` were tracked and were subsequently removed from the Git index using `git rm --cached`.
- **Status:** PASS after that remediation. `git rm --cached` does not erase prior Git history; any real exposed credential must still be rotated.

### Audit D — RBAC and Service-Account Access

- **Control:** The API should not receive Kubernetes API permissions or a service-account token unless it needs them.
- **Observed:** The API Role included `get` and `list` permissions on Pods, and service-account token automounting was enabled by default at the time of the audit.
- **Status:** GAP identified; remediation was tracked for Day 49.

### Audit E — NetworkPolicy Enforcement

- **Control:** NetworkPolicies must be enforced by the cluster's CNI, and required and unauthorized traffic paths must be tested.
- **Observed:** The Minikube environment was configured with Calico; API-to-PostgreSQL and API-to-Redis connectivity succeeded, while the unlabeled BusyBox test pod's connections to those services timed out.
- **Status:** PASS for the tested paths and environment. This did not yet demonstrate default-deny egress or automated CI regression tests.

### Audit F — CI/CD Security Enforcement

- **Control:** Required security checks should enforce the intended policy, and third-party actions should use immutable references.
- **Observed:** Checkov was configured with `soft_fail: true`, making its findings non-blocking. The audit also identified GitHub Actions referenced through mutable tags such as `@master`.
- **Status:** CRITICAL GAP at the time of the audit; remediation remained outstanding after Day 47.

## Day 48 — Secrets Remediation

- **Objective:** Remove hard-coded database credentials from application and deployment configuration.
- **Changes:**
  - Removed the hard-coded database-password fallback from `app.py`.
  - Moved the database password into a Kubernetes Secret.
  - Updated the application/workload configuration to consume the password from the Secret rather than relying on a plaintext fallback.
- **Validation:**
  - Verified that the API connected successfully to PostgreSQL after the change.
  - Checked tracked Git files and verified that the plaintext credential was no longer present in the tracked configuration.
- **Outcome:** The hard-coded-secret finding from Day 47 was remediated in the current configuration. The original Day 47 audit remains the historical record of the finding.

## Day 49 — RBAC and Service-Account Hardening

- **Objective:** Remove unnecessary Kubernetes API access from the Flask API workload.
- **Changes:**
  - Set `automountServiceAccountToken: false` in the API Pod template.
  - Removed the unused API Role and associated RoleBinding from the Helm-managed configuration and cluster.
  - Investigated old API Pods that still had the previous token mount because changing a Deployment's Pod template does not mutate already-running Pods.
  - Updated the Helm source of truth so Helm would stop recreating the removed RBAC resources during reconciliation.
  - Recreated/reconciled the workload using the updated configuration rather than relying only on manual deletion of live resources.
- **Validation:**
  - Confirmed `automountServiceAccountToken` was set to `false` in the API workload configuration.
  - Ran `kubectl auth can-i list pods` for the API ServiceAccount identity; the result was `no`.
- **Outcome:** The unnecessary Pod-list permission and automatic service-account token mounting were removed for the API workload. The troubleshooting also exposed why RBAC changes must be made in Helm's declared source of truth, not only by deleting resources directly from the cluster.