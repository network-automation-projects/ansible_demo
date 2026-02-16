"""
Python Network Automation - Configuration Management Examples
"""

from typing import Dict, Any, List
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ConfigTemplateEngine:
    """Jinja2-based configuration template engine."""
    
    def render(self, template: str, **kwargs) -> str:
        """Render template with variables."""
        # In production: from jinja2 import Template
        # return Template(template).render(**kwargs)
        return template.format(**kwargs)


class DeviceOutputParser:
    """Parse device command output using regex."""
    
    def extract_ips(self, output: str) -> List[str]:
        """Extract IP addresses."""
        pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        return re.findall(pattern, output)
    
    def extract_interfaces(self, output: str) -> List[str]:
        """Extract interface names."""
        pattern = r'(GigabitEthernet|Ethernet|FastEthernet)\d+/\d+'
        return re.findall(pattern, output)


if __name__ == "__main__":
    print("Configuration Management Examples")
    parser = DeviceOutputParser()
    output = "Interface GigabitEthernet0/0 has IP 10.0.0.1"
    ips = parser.extract_ips(output)
    print(f"Found IPs: {ips}")
