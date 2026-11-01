# Day 47: RBAC and Service Account Audit

## Audit D — Identity and Access Management

### Finding 1: Over-privileged API Service Account
- **Control:** The application workload should have no unnecessary access to the Kubernetes API.
- **Expected:** Service account should not be able to list/get pods unless required by the app.
- **Observed:** The `api-role` grants `get` and `list` on `pods` in the `default` namespace.
- **Status:** **GAP**
- **Remaining Risk:** If the API is compromised, an attacker can use the mounted token to enumerate pods in the cluster.

### Finding 2: Automatically Mounted Service Account Token
- **Control:** Workloads that do not need Kubernetes API access should have `automountServiceAccountToken: false`.
- **Expected:** No token mounted inside the container.
- **Observed:** The deployment does not specify `automountServiceAccountToken`, meaning it defaults to `true`.
- **Status:** **GAP**
- **Remaining Risk:** An attacker with code execution inside the container can steal the token from `/var/run/secrets/kubernetes.io/serviceaccount/token`.