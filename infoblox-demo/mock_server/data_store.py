"""In-memory data store for mock Infoblox server."""

import ipaddress
from typing import Any, Dict, List, Optional
import yaml
from pathlib import Path


class DataStore:
    """In-memory data store simulating Infoblox database."""

    def __init__(self):
        """Initialize empty data store."""
        self.dns_records: List[Dict[str, Any]] = []
        self.dhcp_networks: List[Dict[str, Any]] = []
        self.dhcp_ranges: List[Dict[str, Any]] = []
        self.dhcp_reservations: List[Dict[str, Any]] = []
        self.ipam_networks: List[Dict[str, Any]] = []
        self.ipam_ips: Dict[str, Dict[str, Any]] = {}  # IP -> status info
        self._next_ref = 1

    def _generate_ref(self, obj_type: str) -> str:
        """Generate object reference like Infoblox.

        Args:
            obj_type: Object type (e.g., "record:a")

        Returns:
            Object reference string
        """
        ref = f"{obj_type}/Z{self._next_ref}:{obj_type.split(':')[-1]}/default"
        self._next_ref += 1
        return ref

    def load_sample_data(self, data_path: Optional[Path] = None):
        """Load sample data from YAML file.

        Args:
            data_path: Path to mock_data.yaml
        """
        if data_path is None:
            data_path = Path(__file__).parent.parent / "config" / "mock_data.yaml"

        if not data_path.exists():
            return

        with open(data_path) as f:
            data = yaml.safe_load(f)

        # Load networks
        for net in data.get("networks", []):
            net["_ref"] = self._generate_ref("network")
            self.ipam_networks.append(net)

        # Load DNS records
        for record in data.get("dns_records", []):
            record["_ref"] = self._generate_ref(f"record:{record.get('record_type', 'a').lower()}")
            self.dns_records.append(record)

        # Load DHCP ranges
        for range_obj in data.get("dhcp_ranges", []):
            range_obj["_ref"] = self._generate_ref("range")
            self.dhcp_ranges.append(range_obj)

    def add_dns_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Add DNS record to store.

        Args:
            record: DNS record data

        Returns:
            Record with _ref added
        """
        record_type = record.get("record_type", "A").lower()
        if "_ref" not in record:
            record["_ref"] = self._generate_ref(f"record:{record_type}")
        self.dns_records.append(record)
        return record

    def get_dns_records(
        self, filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Get DNS records matching filters.

        Args:
            filters: Filter criteria

        Returns:
            List of matching records
        """
        if not filters:
            return self.dns_records.copy()

        results = []
        for record in self.dns_records:
            match = True
            for key, value in filters.items():
                if record.get(key) != value:
                    match = False
                    break
            if match:
                results.append(record)

        return results

    def delete_dns_record(self, ref: str) -> bool:
        """Delete DNS record by reference.

        Args:
            ref: Object reference

        Returns:
            True if deleted, False if not found
        """
        for i, record in enumerate(self.dns_records):
            if record.get("_ref") == ref:
                del self.dns_records[i]
                return True
        return False

    def add_dhcp_network(self, network: Dict[str, Any]) -> Dict[str, Any]:
        """Add DHCP network to store.

        Args:
            network: Network data

        Returns:
            Network with _ref added
        """
        if "_ref" not in network:
            network["_ref"] = self._generate_ref("network")
        self.dhcp_networks.append(network)
        return network

    def get_dhcp_networks(
        self, filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Get DHCP networks matching filters.

        Args:
            filters: Filter criteria

        Returns:
            List of matching networks
        """
        if not filters:
            return self.dhcp_networks.copy()

        results = []
        for network in self.dhcp_networks:
            match = True
            for key, value in filters.items():
                if network.get(key) != value:
                    match = False
                    break
            if match:
                results.append(network)

        return results

    def add_dhcp_range(self, range_obj: Dict[str, Any]) -> Dict[str, Any]:
        """Add DHCP range to store.

        Args:
            range_obj: Range data

        Returns:
            Range with _ref added
        """
        if "_ref" not in range_obj:
            range_obj["_ref"] = self._generate_ref("range")
        self.dhcp_ranges.append(range_obj)
        return range_obj

    def get_dhcp_ranges(
        self, filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Get DHCP ranges matching filters.

        Args:
            filters: Filter criteria

        Returns:
            List of matching ranges
        """
        if not filters:
            return self.dhcp_ranges.copy()

        results = []
        for range_obj in self.dhcp_ranges:
            match = True
            for key, value in filters.items():
                if range_obj.get(key) != value:
                    match = False
                    break
            if match:
                results.append(range_obj)

        return results

    def add_dhcp_reservation(
        self, reservation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add DHCP reservation to store.

        Args:
            reservation: Reservation data

        Returns:
            Reservation with _ref added
        """
        if "_ref" not in reservation:
            reservation["_ref"] = self._generate_ref("fixedaddress")
        self.dhcp_reservations.append(reservation)
        return reservation

    def get_dhcp_reservations(
        self, filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Get DHCP reservations matching filters.

        Args:
            filters: Filter criteria

        Returns:
            List of matching reservations
        """
        if not filters:
            return self.dhcp_reservations.copy()

        results = []
        for reservation in self.dhcp_reservations:
            match = True
            for key, value in filters.items():
                if reservation.get(key) != value:
                    match = False
                    break
            if match:
                results.append(reservation)

        return results

    def add_ipam_network(self, network: Dict[str, Any]) -> Dict[str, Any]:
        """Add IPAM network to store.

        Args:
            network: Network data

        Returns:
            Network with _ref added
        """
        if "_ref" not in network:
            network["_ref"] = self._generate_ref("network")
        self.ipam_networks.append(network)
        return network

    def get_ipam_networks(
        self, filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Get IPAM networks matching filters.

        Args:
            filters: Filter criteria

        Returns:
            List of matching networks
        """
        if not filters:
            return self.ipam_networks.copy()

        results = []
        for network in self.ipam_networks:
            match = True
            for key, value in filters.items():
                if network.get(key) != value:
                    match = False
                    break
            if match:
                results.append(network)

        return results

    def get_next_available_ip(self, network: str) -> Optional[str]:
        """Get next available IP in network.

        Args:
            network: Network CIDR (e.g., "192.168.1.0/24")

        Returns:
            Next available IP address or None
        """
        try:
            net = ipaddress.IPv4Network(network, strict=False)
            for ip in net.hosts():
                ip_str = str(ip)
                if ip_str not in self.ipam_ips:
                    return ip_str
                if self.ipam_ips[ip_str].get("status") == "AVAILABLE":
                    return ip_str
        except ValueError:
            return None
        return None

    def allocate_ip(
        self, network: str, ip: str, name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Allocate IP address in IPAM.

        Args:
            network: Network CIDR
            ip: IP address
            name: Optional name/comment

        Returns:
            IP allocation record
        """
        allocation = {
            "ipv4addr": ip,
            "network": network,
            "status": "USED",
            "names": [name] if name else [],
            "comment": name,
        }
        self.ipam_ips[ip] = allocation
        return allocation

    def get_ip_status(self, ip: str) -> Optional[Dict[str, Any]]:
        """Get IP address status.

        Args:
            ip: IP address

        Returns:
            IP status information or None
        """
        return self.ipam_ips.get(ip)
