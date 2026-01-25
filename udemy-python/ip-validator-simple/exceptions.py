"""Custom exception classes for IP Validator application.

This module defines simple custom exceptions for better error handling
in IP validation operations.
"""


class IPValidatorError(Exception):
    """Base exception for all IP Validator related errors.
    
    All custom exceptions in this module inherit from this class.
    This allows catching all application-specific errors with a single except clause.
    
    Example:
        try:
            # Some operation
        except IPValidatorError as e:
            # Handle any application error
    """
    
    def __init__(self, message: str):
        """Initialize exception with error message.
        
        Args:
            message: Error message describing what went wrong
        """
        self.message = message
        super().__init__(self.message)


class InvalidIPError(IPValidatorError):
    """Raised when an IP address has invalid format or values.
    
    This exception is raised when:
        - IP format is incorrect (e.g., "999.999.999.999")
        - IP contains non-numeric characters (e.g., "abc.def.ghi")
        - IP has wrong number of octets
        - IP octets are out of valid range (0-255)
    
    Attributes:
        ip_address: The invalid IP address that was provided
        reason: Explanation of why the IP is invalid
    
    Example scenarios:
        - User provides "999.999.999.999" (octets out of range)
        - User provides "192.168.1" (missing octet)
        - User provides "invalid.ip.address" (non-numeric)
    """
    
    def __init__(self, message: str, ip_address: str = None, reason: str = None):
        """Initialize InvalidIPError with details.
        
        Args:
            message: Error message
            ip_address: Optional invalid IP address
            reason: Optional reason why IP is invalid
        """
        super().__init__(message)
        self.ip_address = ip_address
        self.reason = reason


class FileReadError(IPValidatorError):
    """Raised when a file cannot be read.
    
    This exception wraps file-related errors to provide more context
    about which file was expected and why it couldn't be read.
    
    Attributes:
        file_path: Path to the file that couldn't be read
        original_error: The original exception that occurred
    
    Example scenarios:
        - File doesn't exist
        - Permission denied
        - File is a directory
        - File is corrupted or unreadable
    """
    
    def __init__(self, message: str, file_path: str = None, original_error: Exception = None):
        """Initialize FileReadError with details.
        
        Args:
            message: Error message
            file_path: Optional path to the file that couldn't be read
            original_error: Optional original exception that occurred
        """
        super().__init__(message)
        self.file_path = file_path
        self.original_error = original_error

