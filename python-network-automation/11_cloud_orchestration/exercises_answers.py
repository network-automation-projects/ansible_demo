"""
Answer key for exercises.py in this folder.
Use this file to verify your solutions. Same structure as exercises.py with blanks filled in.
"""

from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def list_docker_containers():
    """List Docker containers (requires docker package)."""
    import docker
    client = docker.from_env()
    return client.containers.list()


def list_kubernetes_pods():
    """List Kubernetes pods (requires kubernetes package)."""
    from kubernetes import client, config
    config.load_kube_config()
    v1 = client.CoreV1Api()
    return v1.list_pod_for_all_namespaces()


def create_s3_bucket(bucket_name: str) -> None:
    """Create S3 bucket using Boto3 (requires boto3)."""
    import boto3
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=bucket_name)


if __name__ == "__main__":
    print("11_cloud_orchestration – answer key (run exercises.py to practice)")
