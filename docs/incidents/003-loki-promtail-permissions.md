# Incident 003: Promtail Cannot Read Pod Logs

## Symptom
Promtail running, targets endpoint empty, no logs in Grafana.

## Investigation
1. Checked Promtail logs → "Unable to find any logs to tail"
2. Verified log paths exist on disk → `/var/log/pods/*/*/*.log` present
3. Checked permissions → `drwxr-x---` root-owned directories

## Root Cause
HostPath volumes inherit node permissions. Promtail ran as non-root user (65534). Could not read root-owned log directories.

## Resolution
Added `securityContext: runAsUser: 0` to Promtail Deployment.
Also fixed path glob from 4 levels (`*/*/*/*`) to 3 levels (`*/*/*`).

## Lesson
HostPath + non-root container = permission failure. Always verify file permissions inside the container, not just on the host.
