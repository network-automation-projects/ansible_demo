"""DNS management operations for Infoblox."""

import logging
from typing import List, Optional
from src.infoblox_client import InfobloxClient
from src.models import DNSRecord

logger = logging.getLogger(__name__)


class DNSManager:
    """Manages DNS operations via Infoblox WAPI."""

    def __init__(self, client: InfobloxClient):
        """Initialize DNS manager.

        Args:
            client: InfobloxClient instance
        """
        self.client = client

    def create_a_record(
        self, name: str, ipv4addr: str, comment: Optional[str] = None, ttl: Optional[int] = None
    ) -> DNSRecord:
        """Create an A record.

        Args:
            name: Fully qualified domain name
            ipv4addr: IPv4 address
            comment: Optional comment
            ttl: Optional TTL value

        Returns:
            Created DNSRecord object
        """
        logger.info(f"Creating A record: {name} -> {ipv4addr}")
        data = {"name": name, "ipv4addr": ipv4addr}
        if comment:
            data["comment"] = comment
        if ttl:
            data["ttl"] = ttl

        response = self.client.post("record:a", json_data=data)
        return DNSRecord(
            name=response.get("name", name),
            ipv4addr=response.get("ipv4addr", ipv4addr),
            record_type="A",
            comment=response.get("comment"),
            ttl=response.get("ttl"),
            _ref=response.get("_ref"),
        )

    def create_aaaa_record(
        self, name: str, ipv6addr: str, comment: Optional[str] = None, ttl: Optional[int] = None
    ) -> DNSRecord:
        """Create an AAAA record.

        Args:
            name: Fully qualified domain name
            ipv6addr: IPv6 address
            comment: Optional comment
            ttl: Optional TTL value

        Returns:
            Created DNSRecord object
        """
        logger.info(f"Creating AAAA record: {name} -> {ipv6addr}")
        data = {"name": name, "ipv6addr": ipv6addr}
        if comment:
            data["comment"] = comment
        if ttl:
            data["ttl"] = ttl

        response = self.client.post("record:aaaa", json_data=data)
        return DNSRecord(
            name=response.get("name", name),
            ipv6addr=response.get("ipv6addr", ipv6addr),
            record_type="AAAA",
            comment=response.get("comment"),
            ttl=response.get("ttl"),
            _ref=response.get("_ref"),
        )

    def create_cname(
        self, name: str, canonical: str, comment: Optional[str] = None, ttl: Optional[int] = None
    ) -> DNSRecord:
        """Create a CNAME record.

        Args:
            name: Alias name (FQDN)
            canonical: Canonical name (target FQDN)
            comment: Optional comment
            ttl: Optional TTL value

        Returns:
            Created DNSRecord object
        """
        logger.info(f"Creating CNAME record: {name} -> {canonical}")
        data = {"name": name, "canonical": canonical}
        if comment:
            data["comment"] = comment
        if ttl:
            data["ttl"] = ttl

        response = self.client.post("record:cname", json_data=data)
        return DNSRecord(
            name=response.get("name", name),
            canonical=response.get("canonical", canonical),
            record_type="CNAME",
            comment=response.get("comment"),
            ttl=response.get("ttl"),
            _ref=response.get("_ref"),
        )

    def create_ptr_record(
        self, ipv4addr: str, ptrdname: str, comment: Optional[str] = None, ttl: Optional[int] = None
    ) -> DNSRecord:
        """Create a PTR record (reverse DNS).

        Args:
            ipv4addr: IPv4 address
            ptrdname: PTR domain name
            comment: Optional comment
            ttl: Optional TTL value

        Returns:
            Created DNSRecord object
        """
        logger.info(f"Creating PTR record: {ipv4addr} -> {ptrdname}")
        data = {"ipv4addr": ipv4addr, "ptrdname": ptrdname}
        if comment:
            data["comment"] = comment
        if ttl:
            data["ttl"] = ttl

        response = self.client.post("record:ptr", json_data=data)
        return DNSRecord(
            ipv4addr=response.get("ipv4addr", ipv4addr),
            ptrdname=response.get("ptrdname", ptrdname),
            record_type="PTR",
            comment=response.get("comment"),
            ttl=response.get("ttl"),
            _ref=response.get("_ref"),
        )

    def get_a_records(
        self, name: Optional[str] = None, ipv4addr: Optional[str] = None
    ) -> List[DNSRecord]:
        """Get A records matching criteria.

        Args:
            name: Filter by name
            ipv4addr: Filter by IPv4 address

        Returns:
            List of matching DNSRecord objects
        """
        params = {}
        if name:
            params["name"] = name
        if ipv4addr:
            params["ipv4addr"] = ipv4addr

        response = self.client.get("record:a", params=params)
        records = response if isinstance(response, list) else [response] if response else []

        return [
            DNSRecord(
                name=r.get("name", ""),
                ipv4addr=r.get("ipv4addr"),
                record_type="A",
                comment=r.get("comment"),
                ttl=r.get("ttl"),
                _ref=r.get("_ref"),
            )
            for r in records
        ]

    def get_cname_records(
        self, name: Optional[str] = None, canonical: Optional[str] = None
    ) -> List[DNSRecord]:
        """Get CNAME records matching criteria.

        Args:
            name: Filter by name
            canonical: Filter by canonical name

        Returns:
            List of matching DNSRecord objects
        """
        params = {}
        if name:
            params["name"] = name
        if canonical:
            params["canonical"] = canonical

        response = self.client.get("record:cname", params=params)
        records = response if isinstance(response, list) else [response] if response else []

        return [
            DNSRecord(
                name=r.get("name", ""),
                canonical=r.get("canonical"),
                record_type="CNAME",
                comment=r.get("comment"),
                ttl=r.get("ttl"),
                _ref=r.get("_ref"),
            )
            for r in records
        ]

    def get_ptr_records(
        self, ipv4addr: Optional[str] = None, ptrdname: Optional[str] = None
    ) -> List[DNSRecord]:
        """Get PTR records matching criteria.

        Args:
            ipv4addr: Filter by IPv4 address
            ptrdname: Filter by PTR domain name

        Returns:
            List of matching DNSRecord objects
        """
        params = {}
        if ipv4addr:
            params["ipv4addr"] = ipv4addr
        if ptrdname:
            params["ptrdname"] = ptrdname

        response = self.client.get("record:ptr", params=params)
        records = response if isinstance(response, list) else [response] if response else []

        return [
            DNSRecord(
                ipv4addr=r.get("ipv4addr"),
                ptrdname=r.get("ptrdname"),
                record_type="PTR",
                comment=r.get("comment"),
                ttl=r.get("ttl"),
                _ref=r.get("_ref"),
            )
            for r in records
        ]

    def delete_record(self, ref: str) -> bool:
        """Delete DNS record by reference.

        Args:
            ref: Object reference from Infoblox

        Returns:
            True if deleted successfully
        """
        logger.info(f"Deleting DNS record: {ref}")
        try:
            self.client.delete(ref)
            return True
        except Exception as e:
            logger.error(f"Failed to delete record: {e}")
            return False

    def search_records(self, name: str) -> List[DNSRecord]:
        """Search for all DNS records matching a name.

        Args:
            name: Name to search for

        Returns:
            List of matching DNSRecord objects
        """
        all_records = []
        all_records.extend(self.get_a_records(name=name))
        all_records.extend(self.get_cname_records(name=name))
        return all_records
