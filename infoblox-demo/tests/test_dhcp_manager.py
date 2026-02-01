"""Tests for DHCPManager."""

import pytest
from unittest.mock import Mock
from src.infoblox_client import InfobloxClient
from src.dhcp_manager import DHCPManager


class TestDHCPManager:
    """Test DHCPManager."""

    @pytest.fixture
    def mock_client(self):
        """Create mock InfobloxClient."""
        client = Mock(spec=InfobloxClient)
        return client

    @pytest.fixture
    def dhcp_manager(self, mock_client):
        """Create DHCPManager with mock client."""
        return DHCPManager(mock_client)

    def test_create_network(self, dhcp_manager, mock_client):
        """Test creating DHCP network."""
        mock_response = {
            "network": "192.168.1.0/24",
            "_ref": "network/Z1:network/default",
            "comment": "Production network",
        }
        mock_client.post.return_value = mock_response

        result = dhcp_manager.create_network("192.168.1.0/24", comment="Production network")

        assert result.network == "192.168.1.0/24"
        assert result.comment == "Production network"
        assert result._ref == "network/Z1:network/default"
        mock_client.post.assert_called_once()

    def test_get_networks(self, dhcp_manager, mock_client):
        """Test getting DHCP networks."""
        mock_response = [
            {"network": "192.168.1.0/24", "_ref": "network/Z1:network/default"},
            {"network": "10.0.0.0/16", "_ref": "network/Z2:network/default"},
        ]
        mock_client.get.return_value = mock_response

        results = dhcp_manager.get_networks()

        assert len(results) == 2
        assert results[0].network == "192.168.1.0/24"
        assert results[1].network == "10.0.0.0/16"

    def test_create_range(self, dhcp_manager, mock_client):
        """Test creating DHCP range."""
        mock_response = {
            "start_ip": "192.168.1.100",
            "end_ip": "192.168.1.200",
            "network": "192.168.1.0/24",
            "_ref": "range/Z1:range/default",
        }
        mock_client.post.return_value = mock_response

        result = dhcp_manager.create_range("192.168.1.100", "192.168.1.200", "192.168.1.0/24")

        assert result.start_ip == "192.168.1.100"
        assert result.end_ip == "192.168.1.200"
        assert result.network == "192.168.1.0/24"
        mock_client.post.assert_called_once()

    def test_get_ranges(self, dhcp_manager, mock_client):
        """Test getting DHCP ranges."""
        mock_response = [
            {
                "start_ip": "192.168.1.100",
                "end_ip": "192.168.1.200",
                "network": "192.168.1.0/24",
                "_ref": "range/Z1:range/default",
            }
        ]
        mock_client.get.return_value = mock_response

        results = dhcp_manager.get_ranges()

        assert len(results) == 1
        assert results[0].start_ip == "192.168.1.100"

    def test_create_reservation(self, dhcp_manager, mock_client):
        """Test creating DHCP reservation."""
        mock_response = {
            "ipv4addr": "192.168.1.50",
            "mac": "00:11:22:33:44:55",
            "name": "server-01",
            "_ref": "fixedaddress/Z1:fixedaddress/default",
        }
        mock_client.post.return_value = mock_response

        result = dhcp_manager.create_reservation("192.168.1.50", "00:11:22:33:44:55", name="server-01")

        assert result.ipv4addr == "192.168.1.50"
        assert result.mac == "00:11:22:33:44:55"
        assert result.name == "server-01"
        mock_client.post.assert_called_once()

    def test_get_reservations(self, dhcp_manager, mock_client):
        """Test getting DHCP reservations."""
        mock_response = [
            {
                "ipv4addr": "192.168.1.50",
                "mac": "00:11:22:33:44:55",
                "name": "server-01",
                "_ref": "fixedaddress/Z1:fixedaddress/default",
            }
        ]
        mock_client.get.return_value = mock_response

        results = dhcp_manager.get_reservations()

        assert len(results) == 1
        assert results[0].ipv4addr == "192.168.1.50"

    def test_delete_reservation(self, dhcp_manager, mock_client):
        """Test deleting DHCP reservation."""
        mock_client.delete.return_value = {}

        result = dhcp_manager.delete_reservation("fixedaddress/Z1:fixedaddress/default")

        assert result is True
        mock_client.delete.assert_called_once()

    def test_delete_reservation_failure(self, dhcp_manager, mock_client):
        """Test deleting DHCP reservation with failure."""
        mock_client.delete.side_effect = Exception("Not found")

        result = dhcp_manager.delete_reservation("fixedaddress/Z1:fixedaddress/default")

        assert result is False
