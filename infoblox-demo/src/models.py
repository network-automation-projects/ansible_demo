"""Data models for Infoblox objects."""

from dataclasses import dataclass, field
from typing import Dict, Optional, List


@dataclass
class DNSRecord:
    """Represents a DNS record."""

    name: str
    ipv4addr: Optional[str] = None
    ipv6addr: Optional[str] = None
    canonical: Optional[str] = None
    ptrdname: Optional[str] = None
    record_type: str = "A"
    zone: Optional[str] = None
    comment: Optional[str] = None
    ttl: Optional[int] = None
    extattrs: Dict[str, str] = field(default_factory=dict)
    _ref: Optional[str] = None  # Infoblox object reference


@dataclass
class DHCPNetwork:
    """Represents a DHCP network."""

    network: str
    comment: Optional[str] = None
    extattrs: Dict[str, str] = field(default_factory=dict)
    _ref: Optional[str] = None


@dataclass
class DHCPRange:
    """Represents a DHCP range."""

    start_ip: str
    end_ip: str
    network: str
    comment: Optional[str] = None
    extattrs: Dict[str, str] = field(default_factory=dict)
    _ref: Optional[str] = None


@dataclass
class DHCPReservation:
    """Represents a DHCP reservation."""

    ipv4addr: str
    mac: str
    name: Optional[str] = None
    comment: Optional[str] = None
    extattrs: Dict[str, str] = field(default_factory=dict)
    _ref: Optional[str] = None


@dataclass
class IPAMNetwork:
    """Represents an IPAM network."""

    network: str
    comment: Optional[str] = None
    extattrs: Dict[str, str] = field(default_factory=dict)
    _ref: Optional[str] = None


@dataclass
class IPAddress:
    """Represents an IP address in IPAM."""

    ipv4addr: str
    network: str
    status: str = "USED"  # USED, AVAILABLE, RESERVED
    names: List[str] = field(default_factory=list)
    comment: Optional[str] = None
    extattrs: Dict[str, str] = field(default_factory=dict)
    _ref: Optional[str] = None
