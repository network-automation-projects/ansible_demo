###########
# IMPORTS #
###########

from dataclasses import dataclass
import hvac
import os
from hvac.api.system_backend.wrapping import Wrapping
import requests

###################
# IMPORT ENV VARS #
###################

VAULT_ADDRESS = os.environ.get('VAULT_ADDRESS')
VAULT_APPROLE_ROLE_ID = os.environ.get('VAULT_APPROLE_ROLE_ID')
VAULT_APPROLE_SECRET_ID_FILE = os.environ.get('VAULT_APPROLE_SECRET_ID_FILE')
VAULT_API_KEY_PATH = os.environ.get('VAULT_API_KEY_PATH')
VAULT_API_KEY_FIELD = os.environ.get('VAULT_API_KEY_FIELD')
SECURE_SERVICE_ENDPOINT = os.environ.get('SECURE_SERVICE_ENDPOINT')

#######################
# SET UP APPROLE AUTH #
#######################

# Read the content of /tmp/secret and trim the whitespaces
with open('/tmp/secret', 'r') as file:
    wrapped_token = file.read().replace('\n', '')

# Print the wrapped token from the file
print(f'Wrapped token: {wrapped_token}')

# Create a hvac.Client object using wrapped token
client = hvac.Client(
    url=VAULT_ADDRESS,
    token=wrapped_token
)

# Use unwrap method, pass client
unwrapped_data = Wrapping.unwrap(client)

# Print the response
print(f'unwrapped_data: {unwrapped_data}')

# Get the secret_id from the response
secret_id = unwrapped_data['data']['secret_id']

# Print the secret_id
print(f'Secret ID: {secret_id}')

# Authenticate with auth.approle.login
client.auth.approle.login(
    role_id=VAULT_APPROLE_ROLE_ID,
    secret_id=secret_id,
)

# Print authentication status
print(f'Authenticated with role_id and secret_id: {client.is_authenticated()}')

###################################################
# GET SECRET API KEY and POST TO A SECURE SERVICE #
###################################################

# Get the secret version for VAULT_API_KEY_PATH
secret_version_response = client.secrets.kv.v2.read_secret_version(
    mount_point='kv-v2',
    path=VAULT_API_KEY_PATH
)

# Print secret_version_response
print(f'secret_version_response: {secret_version_response}')

# Get api key from response
api_key = secret_version_response['data']['data'][VAULT_API_KEY_FIELD]

# Print API key
print(f'api_key: {api_key}')

# POST to an API, use SECURE_SERVICE_ENDPOINT
url = f'{SECURE_SERVICE_ENDPOINT}'
# Set X-API-KEY in header to api_key
headers = {
    'X-API-KEY': f'{api_key}'
}
# Create a POST request
response = requests.post(url, headers=headers)

# Print response JSON
print(f'Server response: {response.json()}')

