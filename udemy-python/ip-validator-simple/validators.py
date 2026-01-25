"""Input validation functions for IP Validator application.

This module provides validation functions to check IP addresses before processing.
All functions raise appropriate exceptions from exceptions.py when validation fails.
"""

from exceptions import InvalidIPError


def validate_ip_format(ip: str) -> bool:
    """Check if IP matches valid format (four octets separated by dots).
    
    This function checks:
        1. IP is not None or empty
        2. IP contains exactly four octets separated by dots
        3. Each octet contains only digits
    
    Args:
        ip: String IP address to validate
        
    Returns:
        True if IP format is valid
        
    Raises:
        InvalidIPError: If IP format is invalid
        
    Example error scenarios:
        - None input: raise InvalidIPError("IP address cannot be None")
        - Empty string: raise InvalidIPError("IP address cannot be empty")
        - Wrong number of octets: raise InvalidIPError("IP must have exactly 4 octets")
        - Non-numeric characters: raise InvalidIPError("IP contains non-numeric characters")
    """
    if ip is None:
        raise InvalidIPError("IP address cannot be None", ip_address=ip, reason="None value provided")
    
    if not isinstance(ip, str):
        raise InvalidIPError(f"IP address must be a string, got {type(ip).__name__}", ip_address=str(ip))
    
    ip = ip.strip()
    
    if not ip:
        raise InvalidIPError("IP address cannot be empty", ip_address=ip, reason="Empty string provided")
    
    # Split by dots
    octets = ip.split('.')
    
    if len(octets) != 4:
        raise InvalidIPError(
            f"IP must have exactly 4 octets, got {len(octets)}",
            ip_address=ip,
            reason=f"Expected 4 octets, found {len(octets)}"
        )
    
    # Check each octet contains only digits
    for octet in octets:
        if not octet.isdigit():
            raise InvalidIPError(
                f"IP contains non-numeric characters: '{octet}'",
                ip_address=ip,
                reason=f"Non-numeric octet: '{octet}'"
            )
    
    return True


def is_valid_ip(ip: str) -> bool:
    """Validate IP is in valid range (0-255 per octet).
    
    This function checks:
        1. IP format is valid (using validate_ip_format)
        2. Each octet is in valid range (0-255)
    
    Args:
        ip: String IP address to validate
        
    Returns:
        True if IP is valid
        
    Raises:
        InvalidIPError: If IP format is invalid or octets are out of range
        
    Example error scenarios:
        - Octet > 255: raise InvalidIPError("Octet value 999 is out of range (0-255)")
        - Octet < 0: raise InvalidIPError("Octet value -1 is out of range (0-255)")
    """
    # First validate format
    validate_ip_format(ip)
    
    ip = ip.strip()
    octets = ip.split('.')
    
    # Check each octet is in valid range
    for i, octet_str in enumerate(octets):
        try:
            octet_value = int(octet_str)
        except ValueError:
            raise InvalidIPError(
                f"Octet '{octet_str}' is not a valid number",
                ip_address=ip,
                reason=f"Invalid octet at position {i+1}: '{octet_str}'"
            )
        
        if octet_value < 0 or octet_value > 255:
            raise InvalidIPError(
                f"Octet value {octet_value} is out of range (0-255)",
                ip_address=ip,
                reason=f"Octet at position {i+1} ({octet_value}) is out of valid range"
            )
    
    return True

