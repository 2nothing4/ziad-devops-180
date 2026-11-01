# Day 47: Container Security & Filesystem Audit

## Audit A — Container Identity and Privileges
- **Control:** Non-root execution
  - **Expected:** UID 10001
  - **Observed:** UID 10001 (appuser)
  - **Evidence:** `kubectl exec deploy/api -- id`
  - **Status:** PASS
- **Control:** Dropped capabilities
  - **Expected:** CapEff = 0000000000000000
  - **Observed:** CapEff = 0000000000000000
  - **Evidence:** `kubectl exec deploy/api -- sh -c "grep CapEff /proc/1/status"`
  - **Status:** PASS

## Audit B — Filesystem Restrictions
- **Control:** Read-only root filesystem
  - **Expected:** `/app` is not writable
  - **Observed:** `touch: cannot touch '/app/day47-test.txt': Read-only file system`
  - **Status:** PASS
- **Control:** Writable temporary storage
  - **Expected:** `/tmp` is writable via emptyDir
  - **Observed:** `WRITE_OK`
  - **Status:** PASS