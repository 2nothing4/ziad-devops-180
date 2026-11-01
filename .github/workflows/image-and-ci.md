# Day 47: Image and CI Security Audit

## Audit F — CI/CD Pipeline Hygiene

### Finding 1: Checkov Enforcement
- **Control:** Security scans must block the pipeline on failure.
- **Expected:** `soft_fail: false` (or omitted).
- **Observed:** `soft_fail: true` in `.github/workflows/security.yml`.
- **Status:** **CRITICAL GAP**
- **Remaining Risk:** Vulnerable infrastructure or container code can be merged and deployed because the security gate is non-blocking.

### Finding 2: Mutable Action Tags
- **Control:** Third-party GitHub Actions should be pinned to immutable commit SHAs or specific versions.
- **Expected:** `aquasecurity/trivy-action@<version>` and `bridgecrewio/checkov-action@<version>`.
- **Observed:** Both use `@master`.
- **Status:** **GAP**
- **Remaining Risk:** Supply chain attack vector. If the `master` branch is compromised, our pipeline executes malicious code.