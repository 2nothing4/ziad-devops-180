# Incident 002: Alertmanager Webhook Unreachable

## Symptom
Alertmanager could not deliver alerts to webhook receiver.

## Investigation
Checked Alertmanager logs → connection timeout to `host.minikube.internal`.

## Root Cause
`host.minikube.internal` resolved to wrong network interface on WSL2.
Host networking is unreliable for in-cluster → host communication.

## Resolution
Deployed alert receiver as in-cluster Pod with Kubernetes Service.
Alertmanager now routes via cluster DNS (`http://alert-receiver:5000`).

## Lesson
In-cluster services should communicate via cluster DNS, not host networking.
