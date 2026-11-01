# 004: PostgreSQL Outage and Recovery (Kubernetes)

## Objective
Verify that Kubernetes readiness and liveness behave independently during a database outage, and prove that the system recovers without restarting healthy containers.

## Baseline
- API Pods: 3/3 Ready
- API Restart Counts: 0
- PostgreSQL: Running
- `/livez`: 200 OK
- `/readyz`: 200 OK

## Experiment B: Database Outage
- **Action:** Scaled PostgreSQL deployment to 0 replicas.
- **Observation:** API Pods transitioned to `0/1` (NotReady). 
- **Restart Counts:** Remained at **0**. Containers were not killed.
- **`/livez` Result:** 200 OK (Process remained alive).
- **`/readyz` Result:** 503 Service Unavailable (Dependency gone).

## Experiment C: Database Recovery
- **Action:** Scaled PostgreSQL deployment back to 1 replica.
- **Observation:** PostgreSQL became Ready. API Pods automatically transitioned back to `1/1` (Ready).
- **Restart Counts:** Remained at **0**. No unnecessary restarts.
- **`/readyz` Result:** Returned to 200 OK (Traffic resumed).

## Conclusion
The separation of `/livez` and `/readyz` worked perfectly. Kubernetes removed the API pods from the Service endpoints during the outage, preventing 502/503 errors from reaching the user, while keeping the application containers alive to recover instantly when the database returned.