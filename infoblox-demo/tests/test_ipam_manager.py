"""Tests for IPAMManager."""

import pytest
from unittest.mock import Mock
from src.infoblox_client import InfobloxClient
from src.ipam_manager import IPAMManager


class TestIPAMManager:
    """Test IPAMManager."""

    @pytest.fixture
    def mock_client(self):
        """Create mock InfobloxClient."""
        client = Mock(spec=InfobloxClient)
        return client

    @pytest.fixture
    def ipam_manager(self, mock_client):
        """Create IPAMManager with mock client."""
        return IPAMManager(mock_client)

    def test_create_network(self, ipam_manager, mock_client):
        """Test creating IPAM network."""
        mock_response = {
            "network": "192.168.1.0/24",
            "_ref": "network/Z1:network/default",
            "comment": "Production network",
        }
        mock_client.post.return_value = mock_response

        result = ipam_manager.create_network("192.168.1.0/24", comment="Production network")

        assert result.network == "192.168.1.0/24"
        assert result.comment == "Production network"
        assert result._ref == "network/Z1:network/default"
        mock_client.post.assert_called_once()

    def test_get_networks(self, ipam_manager, mock_client):
        """Test getting IPAM networks."""
        mock_response = [
            {"network": "192.168.1.0/24", "_ref": "network/Z1:network/default"},
            {"network": "10.0.0.0/16", "_ref": "network/Z2:network/default"},
        ]
        mock_client.get.return_value = mock_response

        results = ipam_manager.get_networks()

        assert len(results) == 2
        assert results[0].network == "192.168.1.0/24"

    def test_get_next_available_ip(self, ipam_manager, mock_client):
        """Test getting next available IP."""
        mock_response = {"ipv4addr": "192.168.1.1"}
        mock_client.post.return_value = mock_response

        result = ipam_manager.get_next_available_ip("192.168.1.0/24")

        assert result == "192.168.1.1"
        mock_client.post.assert_called_once()

    def test_get_next_available_ip_not_found(self, ipam_manager, mock_client):
        """Test getting next available IP when none available."""
        mock_client.post.side_effect = Exception("No available IPs")

        result = ipam_manager.get_next_available_ip("192.168.1.0/24")

        assert result is None

    def test_allocate_ip(self, ipam_manager, mock_client):
        """Test allocating IP address."""
        mock_response = {
            "ipv4addr": "192.168.1.10",
            "network": "192.168.1.0/24",
            "status": "USED",
            "names": ["web-server"],
            "_ref": "ipv4address/Z1:ipv4address/default",
        }
        mock_client.post.return_value = mock_response

        result = ipam_manager.allocate_ip("192.168.1.0/24", "192.168.1.10", name="web-server")

        assert result.ipv4addr == "192.168.1.10"
        assert result.network == "192.168.1.0/24"
        assert result.status == "USED"
        assert "web-server" in result.names
        mock_client.post.assert_called_once()

    def test_get_ip_status(self, ipam_manager, mock_client):
        """Test getting IP status."""
        mock_response = [
            {
                "ipv4addr": "192.168.1.10",
                "network": "192.168.1.0/24",
                "status": "USED",
                "names": ["web-server"],
                "_ref": "ipv4address/Z1:ipv4address/default",
            }
        ]
        mock_client.get.return_value = mock_response

        result = ipam_manager.get_ip_status("192.168.1.10")

        assert result is not None
        assert result.ipv4addr == "192.168.1.10"
        assert result.status == "USED"

    def test_get_ip_status_not_found(self, ipam_manager, mock_client):
        """Test getting IP status when not found."""
        mock_client.get.return_value = []

        result = ipam_manager.get_ip_status("192.168.1.10")

        assert result is None

    def test_release_ip(self, ipam_manager, mock_client):
        """Test releasing IP address."""
        # Mock get_ip_status to return an IP with a ref
        mock_ip_status = Mock()
        mock_ip_status._ref = "ipv4address/Z1:ipv4address/default"
        mock_ip_status.ipv4addr = "192.168.1.10"
        mock_ip_status.network = "192.168.1.0/24"
        mock_ip_status.status = "USED"
        mock_ip_status.names = []
        mock_ip_status.comment = None

        ipam_manager.get_ip_status = Mock(return_value=mock_ip_status)
        mock_client.delete.return_value = {}

        result = ipam_manager.release_ip("192.168.1.10")

        assert result is True
        mock_client.delete.assert_called_once()

    def test_release_ip_not_found(self, ipam_manager, mock_client):
        """Test releasing IP address when not found."""
        ipam_manager.get_ip_status = Mock(return_value=None)

        result = ipam_manager.release_ip("192.168.1.10")

        assert result is False

    def test_list_all_networks(self, ipam_manager, mock_client):
        """Test listing all networks."""
        mock_response = [
            {"network": "192.168.1.0/24", "_ref": "network/Z1:network/default"},
            {"network": "10.0.0.0/16", "_ref": "network/Z2:network/default"},
        ]
        mock_client.get.return_value = mock_response

        results = ipam_manager.list_all_networks()

        assert len(results) == 2
