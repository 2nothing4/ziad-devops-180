# Engineering Progress Log

## Day 37 — Configuration Drift (Helm)
- **Objective:** Consolidate Helm charts into one source of truth.
- **Changes:** Moved `ziad-devops-chart` to `helm/ziad-devops`, fixed CI paths, updated `rebuild.sh`.
- **Validation:** Green CI pipeline.

## Day 38 — Automated Cache Testing
- **Objective:** Write actual tests for the `/cache` endpoint to verify Redis success and failure paths.
- **Changes:** Updating `tests/test_app.py` with mock Redis connections.
- **Validation:** `pytest` suite passes locally and in CI.

## Day 39 — Application Hardening
- **Objective:** Prevent API information leakage.
- **Changes:** Replaced raw Python exception strings (`str(e)`) with generic JSON error messages for `/health`, `/logs`, and `/cache`. Added server-side logging.
- **Validation:** Pytest suite updated; 4 tests passed. CI green.

## Day 40 — Cloud Sandboxing & CI/CD
- **Objective:** Fix Render deployment failures caused by path restructuring.
- **Changes:** Updated Docker build context to repository root. Created nested `day9-flask/requirements.txt` (`-r ../requirements.txt`) to resolve Render's root directory sandbox. Fixed curl redirect in GitHub Actions.
- **Validation:** All 4 GitHub Action workflows green (Pytest, Security, CI/CD, Deploy).

## Day 41 — Application Lifecycle
- **Objective:** Remove import-time database initialization.
- **Changes:** Removed top-level `init_db()` from `app.py`. Created `manage_db.py` for explicit initialization. Replaced silent exception handling with bare `raise` to ensure non-zero exit status on failure. Added test for import side-effects.
- **Validation:** 5 tests passed. CI green.

## Day 44 — Kubernetes Security Contexts
- **Objective:** Harden the API container by enforcing least privilege.
- **Changes:** Created a non-root `appuser` (UID 10001) in the Dockerfile. Added Pod and Container `securityContext` to the Helm chart (`runAsNonRoot`, `allowPrivilegeEscalation: false`, dropped `ALL` capabilities).
- **Validation:** `kubectl exec deploy/api -- id` confirms the app runs as `uid=10001(appuser)`. Probes remain healthy.