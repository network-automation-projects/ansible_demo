"""Main entry point for IP Validator application.

This module demonstrates basic error handling patterns for network automation.
"""

import sys

from ip_validator import IPValidator
from exceptions import IPValidatorError, InvalidIPError, FileReadError


def main() -> int:
    """Main function with basic error handling.
    
    This function demonstrates:
        - File reading with error handling
        - IP validation with error handling
        - User-friendly error messages
        - Proper exit codes
    
    Returns:
        Exit code: 0 for success, non-zero for errors
    """
    # Default file path
    file_path = "ip_addresses.txt"
    
    # Allow command line argument for file path
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    
    try:
        # Initialize validator
        validator = IPValidator(file_path)
        
        # Load and validate IPs from file
        print(f"Loading IP addresses from: {file_path}")
        valid_ips = validator.load_ips()
        
        # Display results
        print(f"\n✓ Found {len(valid_ips)} valid IP address(es):")
        for ip in valid_ips:
            binary = validator.convert_to_binary(ip)
            print(f"  {ip:15} → {binary}")
        
        # Display invalid IPs if any
        invalid_ips = validator.get_invalid_ips()
        if invalid_ips:
            print(f"\n✗ Found {len(invalid_ips)} invalid IP address(es):")
            for ip, error in invalid_ips:
                print(f"  {ip:15} → Error: {error}")
        
        if not valid_ips and not invalid_ips:
            print("\n⚠ No IP addresses found in file (file may be empty)")
        
        return 0
    
    except FileReadError as e:
        print(f"\n✗ File Error: {e.message}", file=sys.stderr)
        if e.file_path:
            print(f"  File: {e.file_path}", file=sys.stderr)
        if e.original_error:
            print(f"  Details: {e.original_error}", file=sys.stderr)
        return 1
    
    except InvalidIPError as e:
        print(f"\n✗ Invalid IP Error: {e.message}", file=sys.stderr)
        if e.ip_address:
            print(f"  IP: {e.ip_address}", file=sys.stderr)
        if e.reason:
            print(f"  Reason: {e.reason}", file=sys.stderr)
        return 2
    
    except IPValidatorError as e:
        print(f"\n✗ Validation Error: {e.message}", file=sys.stderr)
        return 3
    
    except KeyboardInterrupt:
        print("\n\n⚠ Operation cancelled by user", file=sys.stderr)
        return 130
    
    except Exception as e:
        print(f"\n✗ Unexpected Error: {type(e).__name__}: {e}", file=sys.stderr)
        return 255


if __name__ == "__main__":
    """Entry point for the application.
    
    Exit codes:
        0: Success
        1: File read error
        2: Invalid IP error
        3: Other validation error
        130: User cancellation (Ctrl+C)
        255: Unexpected error
    """
    exit_code = main()
    sys.exit(exit_code)

