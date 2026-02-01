"""Infoblox WAPI client for REST API interactions."""

import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional
import requests
from requests.auth import HTTPBasicAuth
import yaml

logger = logging.getLogger(__name__)


class InfobloxClientError(Exception):
    """Base exception for Infoblox client errors."""

    pass


class InfobloxAuthenticationError(InfobloxClientError):
    """Raised when authentication fails."""

    pass


class InfobloxAPIError(InfobloxClientError):
    """Raised when API call fails."""

    pass


class InfobloxClient:
    """Client for interacting with Infoblox WAPI."""

    def __init__(
        self,
        url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        wapi_version: str = "v2.12",
        verify_ssl: bool = False,
        timeout: int = 30,
        max_retries: int = 3,
        use_mock: bool = False,
        mock_url: str = "http://localhost:8080",
    ):
        """Initialize Infoblox client.

        Args:
            url: Infoblox server URL (e.g., "https://infoblox.example.com")
            username: Username for authentication
            password: Password for authentication
            wapi_version: WAPI version (default: v2.12)
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            use_mock: Use mock server instead of real Infoblox
            mock_url: Mock server URL
        """
        self.use_mock = use_mock
        if use_mock:
            self.base_url = mock_url
            self.wapi_version = wapi_version
            logger.info(f"Using mock Infoblox server at {mock_url}")
        else:
            if not url:
                raise ValueError("URL is required when not using mock server")
            self.base_url = url.rstrip("/")
            self.wapi_version = wapi_version

        self.wapi_url = f"{self.base_url}/wapi/{self.wapi_version}"
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.max_retries = max_retries

        # Authentication
        if not use_mock:
            self.username = username or os.getenv("INFOBLOX_USERNAME", "")
            self.password = password or os.getenv("INFOBLOX_PASSWORD", "")
            if not self.username or not self.password:
                raise InfobloxAuthenticationError(
                    "Username and password required. "
                    "Set via parameters or INFOBLOX_USERNAME/INFOBLOX_PASSWORD env vars."
                )
            self.auth = HTTPBasicAuth(self.username, self.password)
        else:
            # Mock server uses simple auth
            self.auth = HTTPBasicAuth("admin", "admin")

        # Create session for connection pooling
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.verify = verify_ssl

    @classmethod
    def from_config_file(cls, config_path: Optional[Path] = None) -> "InfobloxClient":
        """Create client from configuration file.

        Args:
            config_path: Path to config YAML file. If None, looks for config/config.yaml

        Returns:
            InfobloxClient instance
        """
        if config_path is None:
            project_root = Path(__file__).parent.parent
            config_path = project_root / "config" / "config.yaml"
            if not config_path.exists():
                config_path = project_root / "config" / "config.example.yaml"

        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path) as f:
            config = yaml.safe_load(f)

        infoblox_config = config.get("infoblox", {})
        return cls(
            url=infoblox_config.get("url"),
            username=infoblox_config.get("username"),
            password=infoblox_config.get("password"),
            wapi_version=infoblox_config.get("wapi_version", "v2.12"),
            verify_ssl=infoblox_config.get("verify_ssl", False),
            timeout=infoblox_config.get("timeout", 30),
            max_retries=infoblox_config.get("max_retries", 3),
            use_mock=infoblox_config.get("use_mock", True),
            mock_url=infoblox_config.get("mock_url", "http://localhost:8080"),
        )

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request to Infoblox WAPI.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "record:a")
            params: Query parameters
            data: Form data
            json_data: JSON data

        Returns:
            Response data as dictionary

        Raises:
            InfobloxAPIError: If request fails
        """
        url = f"{self.wapi_url}/{endpoint}"
        logger.debug(f"{method} {url}")

        for attempt in range(self.max_retries):
            try:
                if method == "GET":
                    response = self.session.get(
                        url, params=params, timeout=self.timeout
                    )
                elif method == "POST":
                    if json_data:
                        response = self.session.post(
                            url, json=json_data, timeout=self.timeout
                        )
                    else:
                        response = self.session.post(
                            url, data=data, timeout=self.timeout
                        )
                elif method == "PUT":
                    response = self.session.put(
                        url, json=json_data, timeout=self.timeout
                    )
                elif method == "DELETE":
                    response = self.session.delete(url, timeout=self.timeout)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                response.raise_for_status()

                # Infoblox returns empty body for DELETE
                if response.status_code == 204 or not response.text:
                    return {}

                return response.json()

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 401:
                    raise InfobloxAuthenticationError(
                        f"Authentication failed: {e.response.text}"
                    ) from e
                if attempt == self.max_retries - 1:
                    raise InfobloxAPIError(
                        f"API request failed: {e.response.status_code} - {e.response.text}"
                    ) from e
                logger.warning(f"Request failed, retrying ({attempt + 1}/{self.max_retries})")

            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise InfobloxAPIError(f"Request failed: {str(e)}") from e
                logger.warning(f"Request failed, retrying ({attempt + 1}/{self.max_retries})")

        raise InfobloxAPIError("Request failed after all retries")

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """GET request to WAPI endpoint.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            Response data
        """
        return self._make_request("GET", endpoint, params=params)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """POST request to WAPI endpoint.

        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data

        Returns:
            Response data
        """
        return self._make_request("POST", endpoint, data=data, json_data=json_data)

    def put(self, endpoint: str, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """PUT request to WAPI endpoint.

        Args:
            endpoint: API endpoint
            json_data: JSON data

        Returns:
            Response data
        """
        return self._make_request("PUT", endpoint, json_data=json_data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE request to WAPI endpoint.

        Args:
            endpoint: API endpoint (usually object reference)

        Returns:
            Empty dict on success
        """
        return self._make_request("DELETE", endpoint)

    def search(
        self, endpoint: str, search_params: Dict[str, Any]
    ) -> list[Dict[str, Any]]:
        """Search for objects using WAPI search.

        Args:
            endpoint: API endpoint (e.g., "record:a")
            search_params: Search parameters (e.g., {"name": "web.example.com"})

        Returns:
            List of matching objects
        """
        # Convert search params to WAPI query format
        query_parts = []
        for key, value in search_params.items():
            query_parts.append(f"{key}:{value}")

        params = {"*": "|".join(query_parts)} if query_parts else {}
        response = self.get(endpoint, params=params)

        # WAPI returns list directly for search results
        if isinstance(response, list):
            return response
        return [response] if response else []
