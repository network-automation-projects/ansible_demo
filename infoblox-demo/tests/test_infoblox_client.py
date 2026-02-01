"""Tests for InfobloxClient."""

import pytest
from unittest.mock import Mock, patch
from src.infoblox_client import (
    InfobloxClient,
    InfobloxClientError,
    InfobloxAuthenticationError,
    InfobloxAPIError,
)


class TestInfobloxClient:
    """Test InfobloxClient."""

    def test_init_mock(self):
        """Test client initialization with mock server."""
        client = InfobloxClient(use_mock=True, mock_url="http://localhost:8080")
        assert client.use_mock is True
        assert client.base_url == "http://localhost:8080"
        assert client.wapi_url == "http://localhost:8080/wapi/v2.12"

    def test_init_real_missing_url(self):
        """Test that real client requires URL."""
        with pytest.raises(ValueError, match="URL is required"):
            InfobloxClient(use_mock=False)

    def test_init_real_missing_credentials(self):
        """Test that real client requires credentials."""
        with pytest.raises(InfobloxAuthenticationError):
            InfobloxClient(use_mock=False, url="https://infoblox.example.com")

    @patch.dict("os.environ", {"INFOBLOX_USERNAME": "test", "INFOBLOX_PASSWORD": "test"})
    def test_init_real_with_env_vars(self):
        """Test client initialization with environment variables."""
        client = InfobloxClient(
            use_mock=False, url="https://infoblox.example.com", username=None, password=None
        )
        assert client.username == "test"
        assert client.password == "test"

    @patch("src.infoblox_client.Path.exists")
    @patch("builtins.open")
    @patch("yaml.safe_load")
    def test_from_config_file(self, mock_yaml, mock_open, mock_exists):
        """Test creating client from config file."""
        mock_exists.return_value = True
        mock_yaml.return_value = {
            "infoblox": {
                "use_mock": True,
                "mock_url": "http://localhost:8080",
                "wapi_version": "v2.12",
            }
        }

        client = InfobloxClient.from_config_file()
        assert client.use_mock is True
        assert client.base_url == "http://localhost:8080"

    @patch("requests.Session.get")
    def test_get_request(self, mock_get):
        """Test GET request."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": "success"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = InfobloxClient(use_mock=True)
        result = client.get("record:a")

        assert result == {"result": "success"}
        mock_get.assert_called_once()

    @patch("requests.Session.post")
    def test_post_request(self, mock_post):
        """Test POST request."""
        mock_response = Mock()
        mock_response.json.return_value = {"_ref": "record:a/Z1:a/default"}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        client = InfobloxClient(use_mock=True)
        result = client.post("record:a", json_data={"name": "test.example.com", "ipv4addr": "192.168.1.10"})

        assert result["_ref"] == "record:a/Z1:a/default"
        mock_post.assert_called_once()

    @patch("requests.Session.delete")
    def test_delete_request(self, mock_delete):
        """Test DELETE request."""
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.text = ""
        mock_response.raise_for_status = Mock()
        mock_delete.return_value = mock_response

        client = InfobloxClient(use_mock=True)
        result = client.delete("record:a/Z1:a/default")

        assert result == {}
        mock_delete.assert_called_once()

    @patch("requests.Session.get")
    def test_get_request_authentication_error(self, mock_get):
        """Test GET request with authentication error."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response
        mock_response.raise_for_status.side_effect = Exception("401")

        client = InfobloxClient(use_mock=True)
        with pytest.raises(InfobloxAuthenticationError):
            client.get("record:a")
