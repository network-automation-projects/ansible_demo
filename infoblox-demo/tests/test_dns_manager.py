"""Tests for DNSManager."""

import pytest
from unittest.mock import Mock, patch
from src.infoblox_client import InfobloxClient
from src.dns_manager import DNSManager


class TestDNSManager:
    """Test DNSManager."""

    @pytest.fixture
    def mock_client(self):
        """Create mock InfobloxClient."""
        client = Mock(spec=InfobloxClient)
        return client

    @pytest.fixture
    def dns_manager(self, mock_client):
        """Create DNSManager with mock client."""
        return DNSManager(mock_client)

    def test_create_a_record(self, dns_manager, mock_client):
        """Test creating A record."""
        mock_response = {
            "name": "web.example.com",
            "ipv4addr": "192.168.1.10",
            "_ref": "record:a/Z1:a/default",
            "comment": "Web server",
        }
        mock_client.post.return_value = mock_response

        result = dns_manager.create_a_record("web.example.com", "192.168.1.10", comment="Web server")

        assert result.name == "web.example.com"
        assert result.ipv4addr == "192.168.1.10"
        assert result.record_type == "A"
        assert result._ref == "record:a/Z1:a/default"
        mock_client.post.assert_called_once()

    def test_create_cname(self, dns_manager, mock_client):
        """Test creating CNAME record."""
        mock_response = {
            "name": "www.example.com",
            "canonical": "web.example.com",
            "_ref": "record:cname/Z2:cname/default",
        }
        mock_client.post.return_value = mock_response

        result = dns_manager.create_cname("www.example.com", "web.example.com")

        assert result.name == "www.example.com"
        assert result.canonical == "web.example.com"
        assert result.record_type == "CNAME"
        mock_client.post.assert_called_once()

    def test_create_ptr_record(self, dns_manager, mock_client):
        """Test creating PTR record."""
        mock_response = {
            "ipv4addr": "192.168.1.10",
            "ptrdname": "web.example.com",
            "_ref": "record:ptr/Z3:ptr/default",
        }
        mock_client.post.return_value = mock_response

        result = dns_manager.create_ptr_record("192.168.1.10", "web.example.com")

        assert result.ipv4addr == "192.168.1.10"
        assert result.ptrdname == "web.example.com"
        assert result.record_type == "PTR"
        mock_client.post.assert_called_once()

    def test_get_a_records(self, dns_manager, mock_client):
        """Test getting A records."""
        mock_response = [
            {"name": "web.example.com", "ipv4addr": "192.168.1.10", "_ref": "record:a/Z1:a/default"},
            {"name": "db.example.com", "ipv4addr": "192.168.1.20", "_ref": "record:a/Z2:a/default"},
        ]
        mock_client.get.return_value = mock_response

        results = dns_manager.get_a_records()

        assert len(results) == 2
        assert results[0].name == "web.example.com"
        assert results[1].name == "db.example.com"
        mock_client.get.assert_called_once()

    def test_get_a_records_with_filter(self, dns_manager, mock_client):
        """Test getting A records with name filter."""
        mock_response = [
            {"name": "web.example.com", "ipv4addr": "192.168.1.10", "_ref": "record:a/Z1:a/default"}
        ]
        mock_client.get.return_value = mock_response

        results = dns_manager.get_a_records(name="web.example.com")

        assert len(results) == 1
        assert results[0].name == "web.example.com"
        mock_client.get.assert_called_once_with("record:a", params={"name": "web.example.com"})

    def test_search_records(self, dns_manager, mock_client):
        """Test searching for records."""
        mock_client.get.side_effect = [
            [{"name": "web.example.com", "ipv4addr": "192.168.1.10", "_ref": "record:a/Z1:a/default"}],
            [{"name": "web.example.com", "canonical": "web.example.com", "_ref": "record:cname/Z2:cname/default"}],
        ]

        results = dns_manager.search_records("web.example.com")

        assert len(results) == 2
        assert results[0].name == "web.example.com"
        assert results[1].name == "web.example.com"

    def test_delete_record(self, dns_manager, mock_client):
        """Test deleting DNS record."""
        mock_client.delete.return_value = {}

        result = dns_manager.delete_record("record:a/Z1:a/default")

        assert result is True
        mock_client.delete.assert_called_once_with("record:a/Z1:a/default")

    def test_delete_record_failure(self, dns_manager, mock_client):
        """Test deleting DNS record with failure."""
        mock_client.delete.side_effect = Exception("Not found")

        result = dns_manager.delete_record("record:a/Z1:a/default")

        assert result is False
