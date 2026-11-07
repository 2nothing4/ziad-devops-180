#!/usr/bin/env bash

set -Eeuo pipefail

# Configuration
TEST_NAMESPACE="net-test"
TEST_POD="test-pod"

DB_NAMESPACE="default"
DB_SERVICE="postgres"
DB_HOST="${DB_SERVICE}.${DB_NAMESPACE}.svc.cluster.local"
DB_PORT="5432"

API_DEPLOYMENT="api"

fail() {
    echo "❌ FAIL: $1" >&2
    exit 1
}

pass() {
    echo "✅ PASS: $1"
}

echo "=========================================="
echo "NetworkPolicy Regression Tests"
echo "=========================================="

# Preflight 1: Check Kubernetes connectivity
command -v kubectl >/dev/null 2>&1 || fail "kubectl is not installed."

kubectl get pod "$TEST_POD" -n "$TEST_NAMESPACE" >/dev/null 2>&1 \
    || fail "Test Pod does not exist."

POD_PHASE=$(kubectl get pod "$TEST_POD" \
    -n "$TEST_NAMESPACE" \
    -o jsonpath='{.status.phase}')

[[ "$POD_PHASE" == "Running" ]] \
    || fail "Test Pod is not Running: $POD_PHASE"

# Preflight 2: Check the PostgreSQL Service and endpoints
kubectl get svc "$DB_SERVICE" -n "$DB_NAMESPACE" >/dev/null 2>&1 \
    || fail "PostgreSQL Service was not found."

ENDPOINTS=$(kubectl get endpoints "$DB_SERVICE" \
    -n "$DB_NAMESPACE" \
    -o jsonpath='{.subsets[*].addresses[*].ip}')

[[ -n "$ENDPOINTS" ]] \
    || fail "PostgreSQL has no ready endpoints. Cannot test network isolation."

# Preflight 3: Ensure the diagnostic tools exist inside BusyBox
kubectl exec -n "$TEST_NAMESPACE" "$TEST_POD" -- \
    sh -c 'command -v nslookup >/dev/null 2>&1 && command -v nc >/dev/null 2>&1' \
    || fail "The test Pod needs both nslookup and nc."

# Test 1: Kubernetes internal DNS
echo ""
echo "Testing Kubernetes service DNS..."

if kubectl exec -n "$TEST_NAMESPACE" "$TEST_POD" -- \
    nslookup "$DB_HOST" >/dev/null 2>&1; then
    pass "PostgreSQL Service DNS resolves."
else
    fail "PostgreSQL Service DNS resolution failed."
fi

# Test 2: Kubernetes API service DNS
if kubectl exec -n "$TEST_NAMESPACE" "$TEST_POD" -- \
    nslookup kubernetes.default.svc.cluster.local >/dev/null 2>&1; then
    pass "Kubernetes API Service DNS resolves."
else
    fail "Kubernetes internal DNS resolution failed."
fi

# Test 3: Positive control - API must reach PostgreSQL
echo ""
echo "Testing allowed API-to-PostgreSQL connectivity..."

if kubectl exec -n "$DB_NAMESPACE" "deploy/$API_DEPLOYMENT" -- \
    python -c "import socket; s=socket.create_connection(('$DB_HOST', $DB_PORT), timeout=3); s.close(); print('Connected')" \
    >/dev/null 2>&1; then
    pass "API can reach PostgreSQL."
else
    fail "API cannot reach PostgreSQL. Check application and database health."
fi

# Test 4: Negative control - test Pod must NOT reach PostgreSQL
echo ""
echo "Testing unauthorized PostgreSQL connectivity..."

set +e
DB_OUTPUT=$(kubectl exec -n "$TEST_NAMESPACE" "$TEST_POD" -- \
    nc -z -v -w 3 "$DB_HOST" "$DB_PORT" 2>&1)
DB_EXIT_CODE=$?
set -e

if [[ "$DB_EXIT_CODE" -eq 0 ]]; then
    fail "Security failure: test Pod successfully reached PostgreSQL."
elif printf '%s' "$DB_OUTPUT" | grep -Eiq 'timed out|operation timed out|connection timed out'; then
    pass "Test Pod connection timed out as expected."
else
    echo "$DB_OUTPUT"
    fail "Connection failed, but a NetworkPolicy timeout was not confirmed."
fi

echo ""
echo "=========================================="
echo "All NetworkPolicy path tests passed."
echo "=========================================="