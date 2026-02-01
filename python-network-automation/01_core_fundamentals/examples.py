"""
Python Network Automation - Core Fundamentals Examples
========================================================

Complete working examples demonstrating essential Python built-ins
in real-world network automation scenarios.
"""

from typing import List, Dict, Any, Optional, Tuple
import logging  # why do we not have to say from __ import logging?
# because it is a built-in module, like print, input, etc.
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================================
# Example 1: Device Pre-Flight Validation
# ============================================================================

def validate_device_preconditions(devices: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """
    Validate that all devices meet preconditions before configuration changes.
    
    Uses all() to ensure all devices are ready, and any() to check for blockers.
    
    Args:
        devices: List of device dictionaries with 'status', 'version', 'interfaces' keys
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    # Check if all devices are reachable
    all_reachable = all(device.get('status') == 'reachable' for device in devices)
    if not all_reachable:
        issues.append("Not all devices are reachable")
    
    # Check if any device has critical errors
    has_critical_errors = any(
        device.get('errors', {}).get('critical', 0) > 0 
        for device in devices
    )
    if has_critical_errors:
        issues.append("Some devices have critical errors")
    
    # Check if all devices have required interfaces up
    all_interfaces_up = all(
        all(intf.get('status') == 'up' for intf in device.get('interfaces', []))
        for device in devices
    )
    #will it still work if we remove the nested all()?
    #yes, it will still work.
    #how would it look without the nested all()?
    # all_interfaces_up = all((intf.get('status') == 'up' for intf in device.get('interfaces', []))
    #     for device in devices
    # )
    #what would be the difference?
    #the difference is that the nested all() is checking if all interfaces are up for each device
    #and if any device has an interface down, then the overall status is down
    #without the nested all(), it is checking if all interfaces are up for all devices
    #and if any device has an interface down, then the overall status is down
    # why is the above nested why within why?
    # because we are checking if all interfaces are up for each device
    # and if any device has an interface down, then the overall status is down
    

    if not all_interfaces_up:
        issues.append("Not all required interfaces are up")
    
    is_valid = len(issues) == 0  # if there are no issues, then the devices are valid
    #was that a fancy if?
    #yes, it was a fancy if statement.
    #how would it normally look?
    # if len(issues) == 0:
    #     is_valid = True
    # else:
    #     is_valid = False

    return is_valid, issues


# ============================================================================
# Example 2: Latency Monitoring and Alerting
# ============================================================================

def analyze_latency_metrics(baseline_latencies: Dict[str, float], 
                           current_latencies: Dict[str, float],
                           threshold_ms: float = 10.0) -> Dict[str, Any]:
    """
    Analyze latency variations and identify anomalies.
    
    Uses abs() to calculate absolute differences, max() to find peaks.
    
    Args:
        baseline_latencies: Baseline latency values by device
        current_latencies: Current latency values by device
        threshold_ms: Threshold for alerting in milliseconds
        
    Returns:
        Dictionary with analysis results
    """
    variations = {}
    alerts = []
    
    for device_name in baseline_latencies:
        if device_name not in current_latencies:
            alerts.append(f"{device_name}: No current data")
            continue
        
        baseline = baseline_latencies[device_name]
        current = current_latencies[device_name]
        
        # Calculate absolute variation
        variation = abs(current - baseline)
        variations[device_name] = variation
        
        # Alert if variation exceeds threshold
        if variation > threshold_ms:
            alerts.append(
                f"{device_name}: Latency variation {variation:.2f}ms "
                f"(baseline: {baseline:.2f}ms, current: {current:.2f}ms)"
            )
    
    # Find peak variation
    peak_variation = max(variations.values()) if variations else 0.0
    peak_device = max(variations.items(), key=lambda x: x[1])[0] if variations else None
    # what is the lambda function doing?
    # the lambda function is a anonymous function that is used to find the key of the maximum value in the variations dictionary
    # so the max finds the max, the lambda finds the key of the maximum value    
    
    return {
        'variations': variations,
        'peak_variation': peak_variation,
        'peak_device': peak_device,
        'alerts': alerts,
        'alert_count': len(alerts)
    }


# ============================================================================
# Example 3: Device Provisioning with Sequential IPs
# ============================================================================

def provision_devices(device_names: List[str], 
                     base_subnet: str = "10.0.0.",
                     start_ip: int = 1) -> Dict[str, Dict[str, str]]:
    """
    Provision devices with sequential IP addresses and management configs.
    
    Uses enumerate() to assign sequential IPs and zip() to combine data.
    
    Args:
        device_names: List of device hostnames to provision
        base_subnet: Base subnet for IP assignment (e.g., "10.0.0.")
        start_ip: Starting IP number
        
    Returns:
        Dictionary mapping device names to configuration dictionaries
    """
    configs = {}
    
    # Assign sequential IPs using enumerate
    for index, device_name in enumerate(device_names, start=start_ip):
        ip_address = f"{base_subnet}{index}"
        configs[device_name] = {
            'hostname': device_name,
            'ip_address': ip_address,
            'mgmt_interface': 'GigabitEthernet0/0',
            'status': 'provisioned'
        }
        logger.info(f"Provisioned {device_name} with IP {ip_address}")
    
    return configs


# ============================================================================
# Example 4: Filtering Devices for Maintenance
# ============================================================================

def find_devices_for_maintenance(devices: List[Dict[str, Any]], 
                                 min_uptime_days: int = 30) -> List[Dict[str, Any]]:
    """
    Find devices that need maintenance based on uptime.
    
    Uses filter() to select devices, min() to find minimum uptime.
    
    Args:
        devices: List of device dictionaries with 'uptime_days' key
        min_uptime_days: Minimum uptime threshold for maintenance
        
    Returns:
        List of devices needing maintenance
    """
    # Filter devices with uptime less than threshold
    maintenance_candidates = list(
        filter(lambda d: d.get('uptime_days', 0) < min_uptime_days, devices)
    )
    
    # Find device with minimum uptime
    if maintenance_candidates:
        min_uptime_device = min(maintenance_candidates, key=lambda d: d.get('uptime_days', 0))
        logger.info(
            f"Found {len(maintenance_candidates)} devices for maintenance. "
            f"Minimum uptime: {min_uptime_device.get('hostname')} "
            f"({min_uptime_device.get('uptime_days')} days)"
        )
    
    return maintenance_candidates


# ============================================================================
# Example 5: Transforming Device Data
# ============================================================================

def transform_device_inventory(raw_devices: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Transform raw device data into standardized format.
    
    Uses map() to transform data structures.
    
    Args:
        raw_devices: List of raw device dictionaries
        
    Returns:
        List of standardized device dictionaries
    """
    def standardize_device(device: Dict[str, Any]) -> Dict[str, str]:
        """Standardize a single device record."""
        return {
            'hostname': str(device.get('hostname', 'unknown')),
            'vendor': str(device.get('vendor', 'unknown')).lower(),
            'model': str(device.get('model', 'unknown')),
            'ip_address': str(device.get('ip', '0.0.0.0')),
            'status': str(device.get('status', 'unknown')).lower()
        }
    
    standardized = list(map(standardize_device, raw_devices))
    logger.info(f"Transformed {len(standardized)} devices")
    return standardized


# ============================================================================
# Example 6: Sorting and Prioritizing Devices
# ============================================================================

def prioritize_devices(devices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort devices by priority and criticality.
    
    Uses sorted() with custom key function.
    
    Args:
        devices: List of device dictionaries with 'priority' and 'critical' keys
        
    Returns:
        Sorted list (highest priority first)
    """
    def priority_key(device: Dict[str, Any]) -> Tuple[bool, int]:
        """Key function: critical devices first, then by priority."""
        is_critical = device.get('critical', False)
        priority = device.get('priority', 0)
        # Return tuple: (not is_critical, -priority)
        # False sorts before True, so critical (False) comes first
        # Negative priority so higher numbers sort first
        return (not is_critical, -priority)
    
    sorted_devices = sorted(devices, key=priority_key)
    logger.info(f"Prioritized {len(sorted_devices)} devices")
    return sorted_devices


# ============================================================================
# Example 7: Bandwidth Aggregation
# ============================================================================

def calculate_network_capacity(interfaces: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Calculate total network capacity and utilization.
    
    Uses sum() for aggregation, max() for peak values.
    
    Args:
        interfaces: List of interface dictionaries with bandwidth data
        
    Returns:
        Dictionary with capacity metrics
    """
    # Extract bandwidth values
    bandwidths = [intf.get('bandwidth_mbps', 0) for intf in interfaces]
    utilized = [intf.get('utilized_mbps', 0) for intf in interfaces]
    
    # Calculate totals
    total_capacity = sum(bandwidths)
    total_utilized = sum(utilized)
    
    # Find peak utilization
    peak_utilization = max(utilized) if utilized else 0.0
    peak_interface = interfaces[utilized.index(peak_utilization)] if utilized else None
    
    utilization_percent = (total_utilized / total_capacity * 100) if total_capacity > 0 else 0.0
    
    return {
        'total_capacity_mbps': total_capacity,
        'total_utilized_mbps': total_utilized,
        'utilization_percent': round(utilization_percent, 2),
        'peak_utilization_mbps': peak_utilization,
        'peak_interface': peak_interface.get('name') if peak_interface else None
    }


# ============================================================================
# Example 8: Type-Safe API Response Handling
# ============================================================================

def process_api_response(response: Any) -> Dict[str, Any]:
    """
    Safely process API response with type checking.
    
    Uses isinstance() for type validation, hasattr() for feature detection.
    
    Args:
        response: API response object (could be dict, list, or error)
        
    Returns:
        Processed response dictionary
    """
    # Validate response type
    if not isinstance(response, dict):
        logger.error(f"Invalid response type: {type(response)}")
        return {'error': 'Invalid response format', 'status': 'error'}
    
    # Check for required fields
    required_fields = ['status', 'data']
    missing_fields = [field for field in required_fields if field not in response]
    
    if missing_fields:
        logger.warning(f"Missing fields: {missing_fields}")
        return {'error': f'Missing fields: {missing_fields}', 'status': 'incomplete'}
    
    # Safely access nested data
    status = response.get('status', 'unknown')
    data = response.get('data', {})
    
    # Check if data has expected structure
    if isinstance(data, dict) and hasattr(data, 'keys'):
        device_count = len(data) if hasattr(data, '__len__') else 0
        logger.info(f"Processed API response: status={status}, devices={device_count}")
    
    return {
        'status': status,
        'data': data,
        'processed_at': datetime.now().isoformat()
    }


# ============================================================================
# Example 9: Dynamic Method Invocation
# ============================================================================

class NetworkDevice:
    """Example device class for demonstrating dynamic attribute access."""
    
    def __init__(self, hostname: str, vendor: str):
        self.hostname = hostname
        self.vendor = vendor
        self._facts = {}
    
    def get_facts(self) -> Dict[str, Any]:
        """Get device facts."""
        return self._facts
    
    def get_interfaces(self) -> List[str]:
        """Get interface list."""
        return []
    
    def backup_config(self) -> str:
        """Backup device configuration."""
        return f"Config backup for {self.hostname}"


def safe_device_operation(device: Any, operation: str, default: Any = None) -> Any:
    """
    Safely invoke a device method if it exists.
    
    Uses callable() to check if attribute is callable, getattr() for access.
    
    Args:
        device: Device object
        operation: Method name to invoke
        default: Default value if method doesn't exist
        
    Returns:
        Method result or default value
    """
    # Check if device has the method
    if not hasattr(device, operation):
        logger.warning(f"Device {device.hostname} does not have method {operation}")
        return default
    
    # Get the attribute
    method = getattr(device, operation)
    
    # Check if it's callable
    if not callable(method):
        logger.warning(f"Attribute {operation} is not callable")
        return default
    
    # Invoke the method
    try:
        result = method()
        logger.info(f"Successfully executed {operation} on {device.hostname}")
        return result
    except Exception as e:
        logger.error(f"Error executing {operation} on {device.hostname}: {e}")
        return default


# ============================================================================
# Example 10: Report Formatting
# ============================================================================

def generate_device_report(devices: List[Dict[str, Any]]) -> str:
    """
    Generate a formatted device status report.
    
    Uses format() and str() for string formatting, round() for numbers.
    
    Args:
        devices: List of device dictionaries
        
    Returns:
        Formatted report string
    """
    report_lines = ["=" * 70]
    report_lines.append("DEVICE STATUS REPORT")
    report_lines.append("=" * 70)
    report_lines.append("")
    
    for device in devices:
        hostname = str(device.get('hostname', 'unknown'))
        status = str(device.get('status', 'unknown')).upper()
        cpu = device.get('cpu_percent', 0.0)
        memory = device.get('memory_percent', 0.0)
        
        # Format with appropriate precision
        cpu_str = format(round(cpu, 2), '.2f')
        memory_str = format(round(memory, 2), '.2f')
        
        line = (
            f"Device: {hostname:<20} "
            f"Status: {status:<10} "
            f"CPU: {cpu_str:>6}% "
            f"Memory: {memory_str:>6}%"
        )
        report_lines.append(line)
    
    report_lines.append("")
    report_lines.append(f"Total devices: {len(devices)}")
    report_lines.append("=" * 70)
    
    return "\n".join(report_lines)


# ============================================================================
# Example 11: MAC Address Formatting
# ============================================================================

def format_mac_address(mac_int: int) -> str:
    """
    Format MAC address integer as standard colon-separated hex string.
    
    Uses hex() for conversion, format() for padding.
    
    Args:
        mac_int: MAC address as integer
        
    Returns:
        Formatted MAC address (e.g., "aa:bb:cc:dd:ee:ff")
    """
    # Convert to hex and remove '0x' prefix
    hex_str = hex(mac_int)[2:]
    
    # Pad to 12 characters (6 bytes)
    hex_str = hex_str.zfill(12)
    
    # Insert colons every 2 characters
    mac_parts = [hex_str[i:i+2] for i in range(0, 12, 2)]
    formatted = ":".join(mac_parts)
    
    return formatted


# ============================================================================
# Example 12: Port Range Generation
# ============================================================================

def generate_port_config(start_port: int, end_port: int, step: int = 1) -> List[Dict[str, int]]:
    """
    Generate port configuration for a range of ports.
    
    Uses range() to generate sequences, enumerate() for indexing.
    
    Args:
        start_port: Starting port number
        end_port: Ending port number (inclusive)
        step: Step size for port range
        
    Returns:
        List of port configuration dictionaries
    """
    ports = []
    
    # Generate port numbers using range
    for port_num in range(start_port, end_port + 1, step):
        ports.append({
            'port_number': port_num,
            'vlan': 100 + (port_num % 10),  # Assign VLAN based on port
            'status': 'enabled'
        })
    
    logger.info(f"Generated configuration for {len(ports)} ports")
    return ports


# ============================================================================
# Demonstration
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CORE FUNDAMENTALS EXAMPLES")
    print("=" * 70)
    
    # Example 1: Device validation
    print("\n1. Device Pre-Flight Validation")
    devices = [
        {'status': 'reachable', 'version': '15.1', 'interfaces': [{'status': 'up'}]},
        {'status': 'reachable', 'version': '15.2', 'interfaces': [{'status': 'up'}]},
        {'status': 'unreachable', 'version': '15.1', 'interfaces': [{'status': 'down'}]}
    ]
    is_valid, issues = validate_device_preconditions(devices)
    print(f"Valid: {is_valid}, Issues: {issues}")
    
    # Example 2: Latency analysis
    print("\n2. Latency Analysis")
    baseline = {'router1': 10.5, 'router2': 12.0}
    current = {'router1': 15.2, 'router2': 11.5}
    analysis = analyze_latency_metrics(baseline, current, threshold_ms=3.0)
    print(f"Peak variation: {analysis['peak_variation']}ms")
    print(f"Alerts: {analysis['alerts']}")
    
    # Example 3: Device provisioning
    print("\n3. Device Provisioning")
    device_names = ['router1', 'router2', 'router3']
    configs = provision_devices(device_names, base_subnet='10.0.0.', start_ip=1)
    for name, config in configs.items():
        print(f"{name}: {config['ip_address']}")
    
    # Example 4: Maintenance filtering
    print("\n4. Maintenance Filtering")
    devices = [
        {'hostname': 'r1', 'uptime_days': 45},
        {'hostname': 'r2', 'uptime_days': 15},
        {'hostname': 'r3', 'uptime_days': 60}
    ]
    maintenance = find_devices_for_maintenance(devices, min_uptime_days=30)
    print(f"Devices needing maintenance: {[d['hostname'] for d in maintenance]}")
    
    # Example 5: Data transformation
    print("\n5. Data Transformation")
    raw = [{'hostname': 'R1', 'vendor': 'CISCO', 'model': 'ASR1000', 'ip': '10.0.0.1'}]
    standardized = transform_device_inventory(raw)
    print(standardized)
    
    # Example 6: Prioritization
    print("\n6. Device Prioritization")
    devices = [
        {'hostname': 'r1', 'priority': 3, 'critical': False},
        {'hostname': 'r2', 'priority': 1, 'critical': True},
        {'hostname': 'r3', 'priority': 5, 'critical': False}
    ]
    prioritized = prioritize_devices(devices)
    print([d['hostname'] for d in prioritized])
    
    # Example 7: Bandwidth calculation
    print("\n7. Bandwidth Aggregation")
    interfaces = [
        {'name': 'Eth0', 'bandwidth_mbps': 1000, 'utilized_mbps': 500},
        {'name': 'Eth1', 'bandwidth_mbps': 1000, 'utilized_mbps': 750}
    ]
    capacity = calculate_network_capacity(interfaces)
    print(f"Total capacity: {capacity['total_capacity_mbps']} Mbps")
    print(f"Utilization: {capacity['utilization_percent']}%")
    
    # Example 8: API response processing
    print("\n8. API Response Processing")
    response = {'status': 'success', 'data': {'device1': {}, 'device2': {}}}
    processed = process_api_response(response)
    print(f"Status: {processed['status']}")
    
    # Example 9: Dynamic method invocation
    print("\n9. Dynamic Method Invocation")
    device = NetworkDevice('router1', 'cisco')
    facts = safe_device_operation(device, 'get_facts')
    print(f"Facts retrieved: {facts is not None}")
    
    # Example 10: Report generation
    print("\n10. Report Formatting")
    devices = [
        {'hostname': 'router1', 'status': 'up', 'cpu_percent': 45.678, 'memory_percent': 60.123},
        {'hostname': 'router2', 'status': 'down', 'cpu_percent': 0.0, 'memory_percent': 0.0}
    ]
    report = generate_device_report(devices)
    print(report)
    
    # Example 11: MAC address formatting
    print("\n11. MAC Address Formatting")
    mac = format_mac_address(0xAABBCCDDEEFF)
    print(f"MAC: {mac}")
    
    # Example 12: Port configuration
    print("\n12. Port Range Generation")
    ports = generate_port_config(8000, 8002)
    print(f"Generated {len(ports)} port configs")
    print(ports[0])
