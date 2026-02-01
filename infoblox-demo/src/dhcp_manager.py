"""DHCP management operations for Infoblox."""

import logging
from typing import List, Optional
from src.infoblox_client import InfobloxClient
from src.models import DHCPNetwork, DHCPRange, DHCPReservation

logger = logging.getLogger(__name__)


class DHCPManager:
    """Manages DHCP operations via Infoblox WAPI."""

    def __init__(self, client: InfobloxClient):
        """Initialize DHCP manager.

        Args:
            client: InfobloxClient instance
        """
        self.client = client

    def create_network(
        self, network: str, comment: Optional[str] = None
    ) -> DHCPNetwork:
        """Create a DHCP network.

        Args:
            network: Network CIDR (e.g., "192.168.1.0/24")
            comment: Optional comment

        Returns:
            Created DHCPNetwork object
        """
        logger.info(f"Creating DHCP network: {network}")
        data = {"network": network}
        if comment:
            data["comment"] = comment

        response = self.client.post("network", json_data=data)
        return DHCPNetwork(
            network=response.get("network", network),
            comment=response.get("comment"),
            _ref=response.get("_ref"),
        )

    def get_networks(self, network: Optional[str] = None) -> List[DHCPNetwork]:
        """Get DHCP networks matching criteria.

        Args:
            network: Filter by network CIDR

        Returns:
            List of matching DHCPNetwork objects
        """
        params = {}
        if network:
            params["network"] = network

        response = self.client.get("network", params=params)
        networks = response if isinstance(response, list) else [response] if response else []

        return [
            DHCPNetwork(
                network=n.get("network", ""),
                comment=n.get("comment"),
                _ref=n.get("_ref"),
            )
            for n in networks
        ]

    def create_range(
        self,
        start_ip: str,
        end_ip: str,
        network: str,
        comment: Optional[str] = None,
    ) -> DHCPRange:
        """Create a DHCP range.

        Args:
            start_ip: Starting IP address
            end_ip: Ending IP address
            network: Network CIDR this range belongs to
            comment: Optional comment

        Returns:
            Created DHCPRange object
        """
        logger.info(f"Creating DHCP range: {start_ip}-{end_ip} in {network}")
        data = {
            "start_ip": start_ip,
            "end_ip": end_ip,
            "network": network,
        }
        if comment:
            data["comment"] = comment

        response = self.client.post("range", json_data=data)
        return DHCPRange(
            start_ip=response.get("start_ip", start_ip),
            end_ip=response.get("end_ip", end_ip),
            network=response.get("network", network),
            comment=response.get("comment"),
            _ref=response.get("_ref"),
        )

    def get_ranges(self, network: Optional[str] = None) -> List[DHCPRange]:
        """Get DHCP ranges matching criteria.

        Args:
            network: Filter by network CIDR

        Returns:
            List of matching DHCPRange objects
        """
        params = {}
        if network:
            params["network"] = network

        response = self.client.get("range", params=params)
        ranges = response if isinstance(response, list) else [response] if response else []

        return [
            DHCPRange(
                start_ip=r.get("start_ip", ""),
                end_ip=r.get("end_ip", ""),
                network=r.get("network", ""),
                comment=r.get("comment"),
                _ref=r.get("_ref"),
            )
            for r in ranges
        ]

    def create_reservation(
        self,
        ipv4addr: str,
        mac: str,
        name: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> DHCPReservation:
        """Create a DHCP reservation (static IP assignment).

        Args:
            ipv4addr: IP address to reserve
            mac: MAC address
            name: Optional name/hostname
            comment: Optional comment

        Returns:
            Created DHCPReservation object
        """
        logger.info(f"Creating DHCP reservation: {ipv4addr} for {mac}")
        data = {"ipv4addr": ipv4addr, "mac": mac}
        if name:
            data["name"] = name
        if comment:
            data["comment"] = comment

        response = self.client.post("fixedaddress", json_data=data)
        return DHCPReservation(
            ipv4addr=response.get("ipv4addr", ipv4addr),
            mac=response.get("mac", mac),
            name=response.get("name"),
            comment=response.get("comment"),
            _ref=response.get("_ref"),
        )

    def get_reservations(
        self, ipv4addr: Optional[str] = None, mac: Optional[str] = None
    ) -> List[DHCPReservation]:
        """Get DHCP reservations matching criteria.

        Args:
            ipv4addr: Filter by IP address
            mac: Filter by MAC address

        Returns:
            List of matching DHCPReservation objects
        """
        params = {}
        if ipv4addr:
            params["ipv4addr"] = ipv4addr
        if mac:
            params["mac"] = mac

        response = self.client.get("fixedaddress", params=params)
        reservations = response if isinstance(response, list) else [response] if response else []

        return [
            DHCPReservation(
                ipv4addr=r.get("ipv4addr", ""),
                mac=r.get("mac", ""),
                name=r.get("name"),
                comment=r.get("comment"),
                _ref=r.get("_ref"),
            )
            for r in reservations
        ]

    def delete_reservation(self, ref: str) -> bool:
        """Delete DHCP reservation by reference.

        Args:
            ref: Object reference from Infoblox

        Returns:
            True if deleted successfully
        """
        logger.info(f"Deleting DHCP reservation: {ref}")
        try:
            self.client.delete(ref)
            return True
        except Exception as e:
            logger.error(f"Failed to delete reservation: {e}")
            return False
