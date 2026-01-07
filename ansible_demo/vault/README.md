# Ansible Vault Usage

This directory contains encrypted files for storing sensitive data like passwords, API keys, and other secrets.

## Creating a Vault File

1. **Create a new encrypted vault file:**
   ```bash
   ansible-vault create vault/vault.yml
   ```
   This will prompt you for a vault password and open an editor.

2. **Add your sensitive data:**
   ```yaml
   vault_username: your_username
   vault_password: your_password
   vault_enable_password: your_enable_password
   ```

3. **Save and exit** the editor. The file will be encrypted automatically.

## Using Vault Files

### Method 1: Prompt for Password
```bash
ansible-playbook -i inventories/hosts.yml playbooks/backup_config.yml --ask-vault-pass
```

### Method 2: Use a Password File
Create a password file (keep it secure!):
```bash
echo "your_vault_password" > ~/.vault_pass
chmod 600 ~/.vault_pass
```

Then use it:
```bash
ansible-playbook -i inventories/hosts.yml playbooks/backup_config.yml --vault-password-file ~/.vault_pass
```

### Method 3: Environment Variable
```bash
export ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass
ansible-playbook -i inventories/hosts.yml playbooks/backup_config.yml
```

## Managing Vault Files

- **View encrypted file:**
  ```bash
  ansible-vault view vault/vault.yml
  ```

- **Edit encrypted file:**
  ```bash
  ansible-vault edit vault/vault.yml
  ```

- **Encrypt existing file:**
  ```bash
  ansible-vault encrypt vault/vault.yml
  ```

- **Decrypt file (use with caution!):**
  ```bash
  ansible-vault decrypt vault/vault.yml
  ```

- **Change vault password:**
  ```bash
  ansible-vault rekey vault/vault.yml
  ```

## Using Vault Variables in Playbooks

Reference vault variables in your playbooks:

```yaml
- name: Connect to device
  cisco.ios.ios_command:
    commands: show version
  vars:
    ansible_user: "{{ vault_username }}"
    ansible_password: "{{ vault_password }}"
```

Or in your inventory file:

```yaml
all:
  children:
    cisco_devices:
      hosts:
        router1:
          ansible_user: "{{ vault_username }}"
          ansible_password: "{{ vault_password }}"
```

## Security Best Practices

1. **Never commit** vault password files to version control
2. **Never commit** unencrypted vault files
3. **Use strong passwords** for vault encryption
4. **Restrict access** to vault password files (chmod 600)
5. **Use different vault passwords** for different environments
6. **Rotate vault passwords** regularly

## Example Structure

```
vault/
├── vault.yml              # Encrypted production credentials (not in git)
├── vault.yml.example      # Example structure (safe to commit)
└── README.md              # This file
```

## Troubleshooting

**Error: "Vault password file was not found"**
- Ensure the password file path is correct
- Check file permissions (should be readable)

**Error: "Decryption failed"**
- Verify you're using the correct vault password
- Check if the vault file was corrupted

**Error: "Vault format is unreadable"**
- The file may not be encrypted
- Try encrypting it: `ansible-vault encrypt vault/vault.yml`

