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