"""IPAM (IP Address Management) operations for Infoblox."""

import logging
from typing import List, Optional
from src.infoblox_client import InfobloxClient
from src.models import IPAMNetwork, IPAddress

logger = logging.getLogger(__name__)


class IPAMManager:
    """Manages IPAM operations via Infoblox WAPI."""

    def __init__(self, client: InfobloxClient):
        """Initialize IPAM manager.

        Args:
            client: InfobloxClient instance
        """
        self.client = client

    def create_network(
        self, network: str, comment: Optional[str] = None
    ) -> IPAMNetwork:
        """Create an IPAM network.

        Args:
            network: Network CIDR (e.g., "192.168.1.0/24")
            comment: Optional comment

        Returns:
            Created IPAMNetwork object
        """
        logger.info(f"Creating IPAM network: {network}")
        data = {"network": network}
        if comment:
            data["comment"] = comment

        response = self.client.post("network", json_data=data)
        return IPAMNetwork(
            network=response.get("network", network),
            comment=response.get("comment"),
            _ref=response.get("_ref"),
        )

    def get_networks(self, network: Optional[str] = None) -> List[IPAMNetwork]:
        """Get IPAM networks matching criteria.

        Args:
            network: Filter by network CIDR

        Returns:
            List of matching IPAMNetwork objects
        """
        params = {}
        if network:
            params["network"] = network

        response = self.client.get("network", params=params)
        networks = response if isinstance(response, list) else [response] if response else []

        return [
            IPAMNetwork(
                network=n.get("network", ""),
                comment=n.get("comment"),
                _ref=n.get("_ref"),
            )
            for n in networks
        ]

    def get_next_available_ip(self, network: str) -> Optional[str]:
        """Get next available IP address in a network.

        Args:
            network: Network CIDR

        Returns:
            Next available IP address or None
        """
        logger.info(f"Getting next available IP in {network}")
        try:
            # Use the request endpoint for next available IP
            data = {"network": network}
            response = self.client.post("request", json_data=data)
            return response.get("ipv4addr")
        except Exception as e:
            logger.error(f"Failed to get next available IP: {e}")
            return None

    def allocate_ip(
        self, network: str, ip: str, name: Optional[str] = None, comment: Optional[str] = None
    ) -> IPAddress:
        """Allocate an IP address in IPAM.

        Args:
            network: Network CIDR
            ip: IP address to allocate
            name: Optional name/hostname
            comment: Optional comment

        Returns:
            IPAddress object
        """
        logger.info(f"Allocating IP {ip} in {network}")
        data = {"ip_address": ip, "network": network}
        if name:
            data["names"] = [name]
        if comment:
            data["comment"] = comment

        response = self.client.post("ipv4address", json_data=data)
        return IPAddress(
            ipv4addr=response.get("ipv4addr", ip),
            network=response.get("network", network),
            status=response.get("status", "USED"),
            names=response.get("names", [name] if name else []),
            comment=response.get("comment", comment),
            _ref=response.get("_ref"),
        )

    def get_ip_status(self, ip: str) -> Optional[IPAddress]:
        """Get IP address status.

        Args:
            ip: IP address to check

        Returns:
            IPAddress object or None if not found
        """
        params = {"ip_address": ip}
        response = self.client.get("ipv4address", params=params)
        
        if isinstance(response, list) and response:
            ip_data = response[0]
        elif response:
            ip_data = response
        else:
            return None

        return IPAddress(
            ipv4addr=ip_data.get("ipv4addr", ip),
            network=ip_data.get("network", ""),
            status=ip_data.get("status", "UNKNOWN"),
            names=ip_data.get("names", []),
            comment=ip_data.get("comment"),
            _ref=ip_data.get("_ref"),
        )

    def release_ip(self, ip: str) -> bool:
        """Release an IP address (mark as available).

        Args:
            ip: IP address to release

        Returns:
            True if released successfully
        """
        logger.info(f"Releasing IP: {ip}")
        # In real Infoblox, this would update the IP status
        # For mock, we'll just delete the allocation record
        ip_status = self.get_ip_status(ip)
        if ip_status and ip_status._ref:
            try:
                self.client.delete(ip_status._ref)
                return True
            except Exception as e:
                logger.error(f"Failed to release IP: {e}")
                return False
        return False

    def list_all_networks(self) -> List[IPAMNetwork]:
        """List all IPAM networks.

        Returns:
            List of all IPAMNetwork objects
        """
        return self.get_networks()
