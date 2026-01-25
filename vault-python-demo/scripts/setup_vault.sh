#!/bin/sh
# Setup script for HashiCorp Vault
# This script configures Vault with policies, AppRole auth, and secrets

set -e

echo "=========================================="
echo "Setting up HashiCorp Vault"
echo "=========================================="

# Set Vault address
export VAULT_ADDR='http://127.0.0.1:8200'

# Wait for Vault to be ready
echo "Waiting for Vault to be ready..."
for i in 1 2 3 4 5 6 7 8 9 10; do
    if vault status > /dev/null 2>&1; then
        echo "Vault is ready!"
        break
    fi
    echo "Attempt $i/10: Vault not ready yet, waiting..."
    sleep 2
done

# Check if Vault is ready
if ! vault status > /dev/null 2>&1; then
    echo "ERROR: Vault is not ready. Please check if Vault server is running."
    exit 1
fi

# Step 1: Import policies
echo ""
echo "Step 1: Importing policies..."
vault policy write trusted-orchestrator-policy /vault/config/trusted-orchestrator-policy.hcl
echo "✓ Imported trusted-orchestrator-policy"

vault policy write dev-policy /vault/config/dev-policy.hcl
echo "✓ Imported dev-policy"

# Step 2: Enable AppRole auth method
echo ""
echo "Step 2: Enabling AppRole auth method..."
if vault auth list | grep -q "approle/"; then
    echo "✓ AppRole auth method already enabled"
else
    vault auth enable approle
    echo "✓ Enabled AppRole auth method"
fi

# Step 3: Create AppRole role
echo ""
echo "Step 3: Creating AppRole role..."
vault write auth/approle/role/dev-role \
    token_policies=dev-policy \
    secret_id_ttl=48h \
    token_ttl=48h \
    token_max_ttl=768h
echo "✓ Created dev-role"

# Step 4: Set role_id
echo ""
echo "Step 4: Setting role_id..."
if [ -n "$APPROLE_ROLE_ID" ]; then
    vault write auth/approle/role/dev-role/role-id role_id="${APPROLE_ROLE_ID}"
    echo "✓ Set role_id to: ${APPROLE_ROLE_ID}"
else
    echo "⚠ APPROLE_ROLE_ID not set, using default"
    vault write auth/approle/role/dev-role/role-id role_id="demo-web-app"
    echo "✓ Set role_id to: demo-web-app"
fi

# Step 5: Display role_id for verification
echo ""
echo "Step 5: Verifying role_id..."
vault read auth/approle/role/dev-role/role-id

# Step 6: Create orchestrator token
echo ""
echo "Step 6: Creating orchestrator token..."
if [ -n "$ORCHESTRATOR_TOKEN" ]; then
    vault token create \
        -id="${ORCHESTRATOR_TOKEN}" \
        -policy=trusted-orchestrator-policy \
        -ttl=768h
    echo "✓ Created orchestrator token"
else
    echo "⚠ ORCHESTRATOR_TOKEN not set, creating default token"
    vault token create \
        -id="orchestrator-token-12345" \
        -policy=trusted-orchestrator-policy \
        -ttl=768h
    echo "✓ Created orchestrator token: orchestrator-token-12345"
fi

# Step 7: Enable KV-v2 secrets engine
echo ""
echo "Step 7: Enabling KV-v2 secrets engine..."
if vault secrets list | grep -q "kv-v2/"; then
    echo "✓ KV-v2 secrets engine already enabled"
else
    vault secrets enable -path=kv-v2 kv-v2
    echo "✓ Enabled KV-v2 secrets engine"
fi

# Step 8: Add API key secret
echo ""
echo "Step 8: Adding API key secret..."
vault kv put kv-v2/api-key api-key-descriptor=my-secret-key
echo "✓ Added API key secret"

echo ""
echo "=========================================="
echo "Vault setup completed successfully!"
echo "=========================================="
echo ""
echo "Summary:"
echo "  - Policies imported: trusted-orchestrator-policy, dev-policy"
echo "  - AppRole auth method enabled"
echo "  - AppRole role 'dev-role' created"
echo "  - Orchestrator token created"
echo "  - KV-v2 secrets engine enabled"
echo "  - API key secret stored at kv-v2/api-key"
echo ""

