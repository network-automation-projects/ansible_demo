#!/bin/bash

# Setup script for Ansible Network Automation project
# This script sets up the environment and installs dependencies

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Ansible Network Automation Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}Python version: ${PYTHON_VERSION}${NC}"

# Create virtual environment
echo ""
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}Virtual environment created${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo ""
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate

# Upgrade pip
echo ""
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip --quiet

# Install Python dependencies
echo ""
echo -e "${YELLOW}Installing Python dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    echo -e "${GREEN}Python dependencies installed${NC}"
else
    echo -e "${YELLOW}Warning: requirements.txt not found${NC}"
fi

# Install Ansible collections
echo ""
echo -e "${YELLOW}Installing Ansible collections...${NC}"
if command -v ansible-galaxy &> /dev/null; then
    # Check if requirements.yml exists for collections
    if [ -f "requirements.yml" ]; then
        ansible-galaxy collection install -r requirements.yml
        echo -e "${GREEN}Ansible collections installed${NC}"
    else
        echo -e "${YELLOW}Installing default collections...${NC}"
        ansible-galaxy collection install cisco.ios
        ansible-galaxy collection install ansible.netcommon
        echo -e "${GREEN}Default collections installed${NC}"
    fi
else
    echo -e "${RED}Error: ansible-galaxy not found. Please install Ansible first.${NC}"
    exit 1
fi

# Create necessary directories
echo ""
echo -e "${YELLOW}Creating necessary directories...${NC}"
mkdir -p backups
mkdir -p logs
mkdir -p logs/compliance_reports
mkdir -p logs/device_facts
mkdir -p logs/command_output
echo -e "${GREEN}Directories created${NC}"

# Check Ansible installation
echo ""
echo -e "${YELLOW}Verifying Ansible installation...${NC}"
if command -v ansible-playbook &> /dev/null; then
    ANSIBLE_VERSION=$(ansible-playbook --version | head -n1)
    echo -e "${GREEN}${ANSIBLE_VERSION}${NC}"
else
    echo -e "${RED}Error: ansible-playbook not found${NC}"
    exit 1
fi

# Make scripts executable
echo ""
echo -e "${YELLOW}Making scripts executable...${NC}"
chmod +x run_playbook.sh setup.sh 2>/dev/null || true
echo -e "${GREEN}Scripts are executable${NC}"

# Summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source .venv/bin/activate"
echo ""
echo "2. Configure your inventory:"
echo "   Edit inventories/hosts.yml with your device information"
echo ""
echo "3. (Optional) Set up Ansible Vault:"
echo "   ansible-vault create vault/vault.yml"
echo ""
echo "4. Run a playbook:"
echo "   ./run_playbook.sh playbooks/backup_config.yml"
echo ""
echo -e "${YELLOW}Note: Remember to activate the virtual environment before running playbooks!${NC}"

