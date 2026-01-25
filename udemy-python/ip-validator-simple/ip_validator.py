"""IP address validator with basic error handling.

This module provides the main validator class that handles IP address
validation and conversion operations.
"""

from typing import List
from pathlib import Path

from exceptions import InvalidIPError, FileReadError
from validators import is_valid_ip


class IPValidator:
    """Main validator class for IP address operations.
    
    This class handles loading IPs from a file and validating them
    with basic error handling.
    
    Attributes:
        file_path: Path to the file containing IP addresses
        valid_ips: List of validated IP addresses
        invalid_ips: List of invalid IP addresses with error messages
    """
    
    def __init__(self, file_path: str):
        """Initialize IPValidator with file path.
        
        Args:
            file_path: Path to file containing IP addresses (one per line)
        
        Raises:
            FileReadError: If file_path is invalid or file doesn't exist
        """
        if not file_path:
            raise FileReadError("File path cannot be empty", file_path=file_path)
        
        self.file_path = Path(file_path)
        self.valid_ips: List[str] = []
        self.invalid_ips: List[tuple[str, str]] = []  # (ip, error_message)
    
    def load_ips(self) -> List[str]:
        """Read IPs from file, validate each line.
        
        This method reads the file line by line, validates each IP,
        and stores valid and invalid IPs separately.
        
        Returns:
            List of valid IP addresses
        
        Raises:
            FileReadError: If file cannot be read
        
        Example error scenarios:
            - File not found: raise FileReadError with file path
            - Permission denied: raise FileReadError with permission error
            - Empty file: return empty list (no error)
        """
        try:
            if not self.file_path.exists():
                raise FileReadError(
                    f"File not found: {self.file_path}",
                    file_path=str(self.file_path)
                )
            
            if not self.file_path.is_file():
                raise FileReadError(
                    f"Path is not a file: {self.file_path}",
                    file_path=str(self.file_path)
                )
            
            with open(self.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
        except PermissionError as e:
            raise FileReadError(
                f"Permission denied reading file: {self.file_path}",
                file_path=str(self.file_path),
                original_error=e
            )
        except OSError as e:
            raise FileReadError(
                f"Error reading file: {self.file_path}",
                file_path=str(self.file_path),
                original_error=e
            )
        
        # Process each line
        for line_num, line in enumerate(lines, start=1):
            ip = line.strip()
            
            # Skip empty lines
            if not ip:
                continue
            
            # Validate IP
            try:
                if self.validate_ip(ip):
                    self.valid_ips.append(ip)
            except InvalidIPError as e:
                self.invalid_ips.append((ip, str(e)))
        
        return self.valid_ips
    
    def validate_ip(self, ip: str) -> bool:
        """Validate a single IP address.
        
        This method validates an IP address format and range.
        
        Args:
            ip: IP address string to validate
        
        Returns:
            True if IP is valid
        
        Raises:
            InvalidIPError: If IP format or values are invalid
        """
        return is_valid_ip(ip)
    
    def convert_to_binary(self, ip: str) -> str:
        """Convert IP address to binary format.
        
        Converts each octet to its 8-bit binary representation.
        
        Args:
            ip: Valid IP address string
        
        Returns:
            Binary representation (e.g., "11000000.10101000.00000001.00000001")
        
        Raises:
            InvalidIPError: If IP is invalid
        
        Example:
            convert_to_binary("192.168.1.1")
            Returns: "11000000.10101000.00000001.00000001"
        """
        # Validate IP first
        if not self.validate_ip(ip):
            raise InvalidIPError(f"Cannot convert invalid IP: {ip}", ip_address=ip)
        
        octets = ip.split('.')
        binary_octets = []
        
        for octet_str in octets:
            octet_value = int(octet_str)
            binary_octet = format(octet_value, '08b')  # 8-bit binary with leading zeros
            binary_octets.append(binary_octet)
        
        return '.'.join(binary_octets)
    
    def get_valid_ips(self) -> List[str]:
        """Get list of validated IP addresses.
        
        Returns:
            List of valid IP addresses
        """
        return self.valid_ips.copy()
    
    def get_invalid_ips(self) -> List[tuple[str, str]]:
        """Get list of invalid IP addresses with error messages.
        
        Returns:
            List of tuples (ip_address, error_message)
        """
        return self.invalid_ips.copy()

