#!/usr/bin/env python3
"""
Trusted Orchestrator Service
Generates wrapped secret_id tokens for applications to use for Vault authentication.
This service runs continuously and writes a new wrapped token every 60 seconds.
"""

import os
import time
import hvac

# Environment variables
VAULT_ADDRESS = os.environ.get('VAULT_ADDRESS', 'http://vault-server:8200')
ORCHESTRATOR_TOKEN = os.environ.get('ORCHESTRATOR_TOKEN')
VAULT_APPROLE_ROLE = os.environ.get('VAULT_APPROLE_ROLE', 'dev-role')
SECRET_FILE_PATH = '/tmp/secret'

def wait_for_vault(client, max_retries=30):
    """Wait for Vault to be ready."""
    for i in range(max_retries):
        try:
            if client.sys.is_initialized():
                return True
        except Exception:
            pass
        time.sleep(1)
    return False

def generate_wrapped_token(client, role_name):
    """Generate a wrapped secret_id token."""
    try:
        # Generate secret_id for the role
        response = client.auth.approle.generate_secret_id(
            role_name=role_name,
            wrap_ttl='60s'  # Wrap token valid for 60 seconds
        )
        return response['wrap_info']['token']
    except Exception as e:
        print(f"Error generating wrapped token: {e}")
        return None

def main():
    """Main orchestrator loop."""
    print("Starting Trusted Orchestrator...")
    print(f"Vault Address: {VAULT_ADDRESS}")
    print(f"AppRole Role: {VAULT_APPROLE_ROLE}")
    
    # Create Vault client
    client = hvac.Client(url=VAULT_ADDRESS, token=ORCHESTRATOR_TOKEN)
    
    # Wait for Vault to be ready
    print("Waiting for Vault to be ready...")
    if not wait_for_vault(client):
        print("ERROR: Vault is not ready after 30 seconds")
        return
    
    print("Vault is ready!")
    
    # Main loop: generate wrapped token every 60 seconds
    while True:
        try:
            wrapped_token = generate_wrapped_token(client, VAULT_APPROLE_ROLE)
            if wrapped_token:
                # Write wrapped token to file
                with open(SECRET_FILE_PATH, 'w') as f:
                    f.write(wrapped_token)
                print(f"Generated new wrapped token: {wrapped_token[:20]}...")
            else:
                print("Failed to generate wrapped token")
        except Exception as e:
            print(f"Error in main loop: {e}")
        
        # Wait 60 seconds before generating next token
        time.sleep(60)

if __name__ == '__main__':
    main()

