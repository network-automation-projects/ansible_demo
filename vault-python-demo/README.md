# HashiCorp Vault Learning Project

A comprehensive learning project demonstrating HashiCorp Vault integration with Python using AppRole authentication and the Key/Value secrets engine.

## Overview

This project demonstrates:
- **AppRole Authentication**: Secure authentication using role_id and secret_id
- **Wrapped Tokens**: Single-use tokens provided by a trusted orchestrator
- **KV Secrets Engine**: Storing and retrieving secrets from Vault's Key/Value store
- **Python Integration**: Using the `hvac` library to interact with Vault's API
- **Docker-based Setup**: Self-contained environment matching production-like scenarios

## Architecture

```
┌─────────────────┐
│  Vault Server   │
│  (Port 8200)    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────────┐
│  App  │ │Orchestrator│
│       │ │            │
└───┬───┘ └───┬────────┘
    │         │
    │    ┌────▼────┐
    │    │ /tmp/   │
    │    │ secret  │
    │    └─────────┘
    │
┌───▼──────────┐
│Secure Service│
│  (Port 8080) │
└──────────────┘
```

## Authentication Flow

1. **Trusted Orchestrator** authenticates to Vault using an orchestrator token
2. Orchestrator generates a **wrapped secret_id** token every 60 seconds
3. Wrapped token is written to `/tmp/secret` (shared volume)
4. **Python Application** reads the wrapped token from the file
5. Application **unwraps** the token to get the `secret_id`
6. Application authenticates to Vault using `role_id` + `secret_id`
7. Authenticated application retrieves secrets from KV-v2 engine
8. Application uses the API key to make authenticated requests

## Prerequisites

- Docker and Docker Compose installed
- Basic understanding of HashiCorp Vault concepts
- Python 3.9+ (for local development)

## Quick Start

### 1. Clone/Navigate to Project

```bash
cd ConceptProjects/vault-python-demo
```

### 2. Start Services

```bash
docker-compose up -d
```

This will start:
- Vault server (dev mode) on port 8200
- Trusted orchestrator service
- Python application container
- Secure service (mock API) on port 8080

### 3. Configure Vault

Wait a few seconds for Vault to initialize, then run the setup script:

```bash
docker exec -it lab_vault-server_1 /bin/sh -c "sh /vault/config/../scripts/setup_vault.sh"
```

Or manually configure Vault:

```bash
docker exec -it lab_vault-server_1 /bin/sh
export VAULT_ADDR='http://127.0.0.1:8200'
cd /vault/config

# Import policies
vault policy write trusted-orchestrator-policy /vault/config/trusted-orchestrator-policy.hcl
vault policy write dev-policy /vault/config/dev-policy.hcl

# Enable AppRole
vault auth enable approle

# Create AppRole role
vault write auth/approle/role/dev-role \
    token_policies=dev-policy \
    secret_id_ttl=48h \
    token_ttl=48h \
    token_max_ttl=768h

# Set role_id
vault write auth/approle/role/dev-role/role-id role_id="demo-web-app"

# Create orchestrator token
vault token create \
    -id="orchestrator-token-12345" \
    -policy=trusted-orchestrator-policy \
    -ttl=768h

# Enable KV-v2
vault secrets enable -path=kv-v2 kv-v2

# Add API key secret
vault kv put kv-v2/api-key api-key-descriptor=my-secret-key
```

### 4. Run the Application

Wait for the orchestrator to generate a wrapped token (about 60 seconds), then run:

```bash
docker exec -it lab_app_1 python app.py
```

Expected output:
```
Wrapped token: s.xxxxx...
unwrapped_data: {'data': {'secret_id': '...'}, ...}
Secret ID: xxxxx-xxxxx-xxxxx
Authenticated with role_id and secret_id: True
secret_version_response: {'data': {'data': {'api-key-descriptor': 'my-secret-key'}}, ...}
api_key: my-secret-key
Server response: {'message': 'hello world!'}
```

## Project Structure

```
vault-python-demo/
├── docker-compose.yml              # Container orchestration
├── vault/
│   └── config/
│       ├── dev-policy.hcl          # Policy for accessing KV secrets
│       └── trusted-orchestrator-policy.hcl  # Policy for secret-id generation
├── app/
│   ├── app.py                      # Main Python application
│   ├── requirements.txt            # Python dependencies
│   └── Dockerfile                  # App container definition
├── orchestrator/
│   ├── orchestrator.py             # Token generator service
│   ├── requirements.txt            # Orchestrator dependencies
│   └── Dockerfile                  # Orchestrator container
├── scripts/
│   └── setup_vault.sh              # Vault configuration script
├── .env.example                    # Environment variables template
└── README.md                       # This file
```

## Key Components Explained

### 1. Vault Policies

**dev-policy.hcl**: Grants read and update access to the API key secret
```hcl
path "kv-v2/data/api-key" {
  capabilities = ["read", "update"]
}
```

**trusted-orchestrator-policy.hcl**: Allows generating secret_ids for AppRole
```hcl
path "auth/approle/role/dev-role/secret-id" {
  capabilities = [ "update" ]
}
```

### 2. AppRole Authentication

AppRole is an authentication method that uses:
- **role_id**: Public identifier (can be shared)
- **secret_id**: Secret credential (must be protected)

The trusted orchestrator generates wrapped secret_ids that applications unwrap to authenticate.

### 3. Python Application (`app/app.py`)

The application:
1. Reads wrapped token from `/tmp/secret`
2. Unwraps token to get `secret_id`
3. Authenticates using `role_id` + `secret_id`
4. Retrieves API key from KV-v2 secrets engine
5. Makes authenticated POST request to secure service

### 4. Trusted Orchestrator (`orchestrator/orchestrator.py`)

The orchestrator:
- Authenticates to Vault using orchestrator token
- Generates wrapped secret_id tokens every 60 seconds
- Writes tokens to shared volume for applications to use

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VAULT_ADDRESS` | Vault server URL | `http://vault-server:8200` |
| `VAULT_APPROLE_ROLE_ID` | Role ID for AppRole auth | `demo-web-app` |
| `VAULT_API_KEY_PATH` | Path to API key secret | `api-key` |
| `VAULT_API_KEY_FIELD` | Field name in secret | `api-key-descriptor` |
| `SECURE_SERVICE_ENDPOINT` | Secure service URL | `http://secure-service:8080/api` |
| `ORCHESTRATOR_TOKEN` | Token for orchestrator | `orchestrator-token-12345` |

## Troubleshooting

### Vault not ready
```bash
# Check Vault status
docker exec -it lab_vault-server_1 vault status

# Check logs
docker logs lab_vault-server_1
```

### Invalid wrapped token error
- Wrapped tokens are single-use and expire after 60 seconds
- Wait 60 seconds for orchestrator to generate a new token
- Check orchestrator logs: `docker logs lab_orchestrator_1`

### Authentication failed
- Verify role_id matches: `docker exec -it lab_vault-server_1 vault read auth/approle/role/dev-role/role-id`
- Check AppRole is enabled: `docker exec -it lab_vault-server_1 vault auth list`
- Verify policies are imported: `docker exec -it lab_vault-server_1 vault policy list`

### Cannot read secret
- Verify KV-v2 is enabled: `docker exec -it lab_vault-server_1 vault secrets list`
- Check secret exists: `docker exec -it lab_vault-server_1 vault kv get kv-v2/api-key`
- Verify dev-policy grants access: `docker exec -it lab_vault-server_1 vault policy read dev-policy`

## Key Concepts

### AppRole Authentication Method
- **Purpose**: Machine-to-machine authentication
- **Components**: role_id (public) + secret_id (secret)
- **Use Case**: Applications authenticating to Vault without human intervention

### Wrapped Tokens
- **Purpose**: Secure delivery of secrets
- **Properties**: Single-use, short TTL (60 seconds)
- **Flow**: Orchestrator wraps secret_id → Application unwraps → Gets secret_id

### KV Secrets Engine
- **Version**: KV-v2 (versioned key-value store)
- **Path Structure**: `kv-v2/data/<path>` for reading
- **Capabilities**: Versioning, metadata, soft delete

### Policies
- **Purpose**: Define what authenticated entities can access
- **Syntax**: HCL (HashiCorp Configuration Language)
- **Capabilities**: create, read, update, delete, list, sudo, deny

## Learning Resources

- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
- [AppRole Auth Method](https://www.vaultproject.io/docs/auth/approle)
- [KV Secrets Engine](https://www.vaultproject.io/docs/secrets/kv)
- [hvac Python Library](https://hvac.readthedocs.io/)

## Security Notes

⚠️ **This project uses Vault in dev mode for learning purposes only!**

- Dev mode uses an in-memory backend (data is lost on restart)
- Root token is exposed in environment variables
- Not suitable for production use

For production:
- Use proper storage backend (Consul, etcd, etc.)
- Enable audit logging
- Use proper TLS/SSL
- Implement proper secret rotation
- Use Vault Agent for token management

## Cleanup

Stop and remove all containers:

```bash
docker-compose down -v
```

This will remove:
- All containers
- Volumes (including trusted-orchestrator-volume)
- Networks

## License

This is a learning project for educational purposes.

