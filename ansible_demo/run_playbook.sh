#!/bin/bash

# Helper script to run Ansible playbooks
# Usage: ./run_playbook.sh <playbook_path> [options]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if playbook path is provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Playbook path is required${NC}"
    echo "Usage: $0 <playbook_path> [options]"
    echo ""
    echo "Examples:"
    echo "  $0 playbooks/backup_config.yml"
    echo "  $0 playbooks/gather_facts.yml --ask-vault-pass"
    echo "  $0 playbooks/configure_device.yml -e 'config_lines=[\"hostname NEW_NAME\"]'"
    exit 1
fi

PLAYBOOK="$1"
shift  # Remove first argument, keep the rest for ansible-playbook

# Check if playbook exists
if [ ! -f "$PLAYBOOK" ]; then
    echo -e "${RED}Error: Playbook not found: $PLAYBOOK${NC}"
    exit 1
fi

# Check if ansible-playbook is available
if ! command -v ansible-playbook &> /dev/null; then
    echo -e "${RED}Error: ansible-playbook not found${NC}"
    echo "Please install Ansible or activate your virtual environment"
    exit 1
fi

# Check if inventory exists
if [ ! -f "inventories/hosts.yml" ]; then
    echo -e "${YELLOW}Warning: Inventory file not found at inventories/hosts.yml${NC}"
fi

# Display information
echo -e "${GREEN}Running Ansible playbook:${NC} $PLAYBOOK"
echo -e "${GREEN}Inventory:${NC} inventories/hosts.yml"
echo ""

# Run the playbook
ansible-playbook -i inventories/hosts.yml "$PLAYBOOK" "$@"

# Check exit status
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}Playbook completed successfully!${NC}"
else
    echo ""
    echo -e "${RED}Playbook failed!${NC}"
    exit 1
fi

