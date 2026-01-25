"""
Setup script for deployment orchestrator.
"""

from setuptools import find_packages, setup

setup(
    name="deployctl",
    version="1.0.0",
    description="Deployment Orchestrator - Automate application deployments",
    author="Rebecca Clarke",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.0",
        "pyyaml>=6.0",
        "requests>=2.31.0",
        "docker>=6.1.0",
        "kubernetes>=28.1.0",
        "paramiko>=3.3.0",
        "structlog>=23.2.0",
    ],
    entry_points={
        "console_scripts": [
            "deployctl=deployctl.cli:cli",
        ],
    },
    python_requires=">=3.9",
)
