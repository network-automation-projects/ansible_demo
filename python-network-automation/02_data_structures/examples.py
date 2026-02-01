"""
Python Network Automation - Data Structures Examples
=====================================================

Complete working examples demonstrating advanced Python collections
in real-world network automation scenarios.
"""

from collections import defaultdict, namedtuple, Counter, deque, OrderedDict
from copy import copy, deepcopy
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================================
# Example 1: Grouping Devices by Vendor/Site
# ============================================================================

def group_devices_by_attribute(devices: List[Dict[str, Any]], attribute: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group devices by any attribute using defaultdict.
    
    Uses defaultdict to avoid key existence checks.
    
    Args:
        devices: List of device dictionaries
        attribute: Attribute name to group by (e.g., 'vendor', 'site')
        
    Returns:
        Dictionary mapping attribute value to list of devices
    """
    grouped = defaultdict(list)
    
    for device in devices:
        key = device.get(attribute, 'unknown')
        grouped[key].append(device)
    
    logger.info(f"Grouped {len(devices)} devices by {attribute}: {list(grouped.keys())}")
    return dict(grouped)


# ============================================================================
# Example 2: Structured Device Facts with namedtuple
# ============================================================================

# Define namedtuple for device facts
DeviceFacts = namedtuple('DeviceFacts', [
    'hostname',
    'vendor',
    'model',
    'os_version',
    'serial_number',
    'uptime_seconds'
])


def create_device_facts(device_data: Dict[str, Any]) -> DeviceFacts:
    """
    Create a DeviceFacts namedtuple from device data.
    
    Args:
        device_data: Dictionary with device information
        
    Returns:
        DeviceFacts namedtuple instance
    """
    return DeviceFacts(
        hostname=device_data.get('hostname', 'unknown'),
        vendor=device_data.get('vendor', 'unknown'),
        model=device_data.get('model', 'unknown'),
        os_version=device_data.get('os_version', 'unknown'),
        serial_number=device_data.get('serial_number', 'unknown'),
        uptime_seconds=device_data.get('uptime_seconds', 0)
    )


def process_device_inventory(devices: List[Dict[str, Any]]) -> List[DeviceFacts]:
    """
    Process device inventory into structured facts.
    
    Args:
        devices: List of device dictionaries
        
    Returns:
        List of DeviceFacts namedtuples
    """
    facts_list = [create_device_facts(device) for device in devices]
    logger.info(f"Processed {len(facts_list)} devices into structured facts")
    return facts_list


# ============================================================================
# Example 3: Counting Interface Statuses
# ============================================================================

def analyze_interface_statuses(interfaces: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Analyze interface statuses using Counter.
    
    Args:
        interfaces: List of interface dictionaries with 'status' key
        
    Returns:
        Dictionary with status counts and statistics
    """
    # Count statuses
    statuses = [intf.get('status', 'unknown') for intf in interfaces]
    status_counter = Counter(statuses)
    
    # Calculate statistics
    total = len(interfaces)
    up_count = status_counter.get('up', 0)
    down_count = status_counter.get('down', 0)
    up_percent = (up_count / total * 100) if total > 0 else 0.0
    
    logger.info(
        f"Interface status: {up_count} up, {down_count} down "
        f"({up_percent:.1f}% up)"
    )
    
    return {
        'total': total,
        'status_counts': dict(status_counter),
        'up_count': up_count,
        'down_count': down_count,
        'up_percent': round(up_percent, 2)
    }


# ============================================================================
# Example 4: Telemetry Buffer with deque
# ============================================================================

class TelemetryBuffer:
    """Buffer for recent telemetry data using deque."""
    
    def __init__(self, max_size: int = 1000):
        """
        Initialize telemetry buffer.
        
        Args:
            max_size: Maximum number of entries to store
        """
        self.buffer = deque(maxlen=max_size)
        self.max_size = max_size
    
    def add(self, timestamp: datetime, metric: str, value: float) -> None:
        """
        Add telemetry data point.
        
        Args:
            timestamp: Timestamp of measurement
            metric: Metric name
            value: Metric value
        """
        entry = {
            'timestamp': timestamp,
            'metric': metric,
            'value': value
        }
        self.buffer.append(entry)
    
    def get_recent(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get most recent entries.
        
        Args:
            count: Number of recent entries to return
            
        Returns:
            List of recent entries
        """
        return list(self.buffer)[-count:]
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all entries."""
        return list(self.buffer)
    
    def size(self) -> int:
        """Get current buffer size."""
        return len(self.buffer)


# ============================================================================
# Example 5: Preserving Config Application Order
# ============================================================================

def create_configuration_plan(config_steps: List[Dict[str, str]]) -> OrderedDict:
    """
    Create ordered configuration plan.
    
    Uses OrderedDict to preserve application order.
    
    Args:
        config_steps: List of configuration step dictionaries
        
    Returns:
        OrderedDict mapping step names to commands
    """
    config_plan = OrderedDict()
    
    for step in config_steps:
        step_name = step.get('name')
        command = step.get('command')
        config_plan[step_name] = command
    
    logger.info(f"Created configuration plan with {len(config_plan)} steps")
    return config_plan


def apply_configuration_plan(plan: OrderedDict, device: Any) -> List[str]:
    """
    Apply configuration plan in order.
    
    Args:
        plan: OrderedDict of configuration steps
        device: Device object (mock for example)
        
    Returns:
        List of applied commands
    """
    applied = []
    for step_name, command in plan.items():
        # In real implementation, would send command to device
        logger.info(f"Applying step {step_name}: {command}")
        applied.append(command)
    
    return applied


# ============================================================================
# Example 6: Safe Config Duplication
# ============================================================================

def duplicate_device_config(original_config: Dict[str, Any], deep: bool = True) -> Dict[str, Any]:
    """
    Duplicate device configuration safely.
    
    Args:
        original_config: Original configuration dictionary
        deep: If True, use deepcopy; if False, use shallow copy
        
    Returns:
        Duplicated configuration
    """
    if deep:
        duplicated = deepcopy(original_config)
        logger.info("Created deep copy of configuration")
    else:
        duplicated = copy(original_config)
        logger.warning("Created shallow copy - nested structures are referenced!")
    
    return duplicated


def modify_config_safely(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Modify configuration without affecting original.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Modified configuration (original unchanged)
    """
    # Create deep copy to avoid modifying original
    modified = deepcopy(config)
    
    # Modify the copy
    if 'interfaces' in modified:
        for interface in modified['interfaces']:
            interface['status'] = 'modified'
    
    return modified


# ============================================================================
# Example 7: Error Counting by Device
# ============================================================================

def count_errors_by_device_and_type(logs: List[Dict[str, str]]) -> Dict[str, Counter]:
    """
    Count errors grouped by device and error type.
    
    Uses defaultdict(Counter) for efficient grouped counting.
    
    Args:
        logs: List of log dictionaries with 'device' and 'error_type' keys
        
    Returns:
        Dictionary mapping device to Counter of error types
    """
    device_errors = defaultdict(Counter)
    
    for log in logs:
        device = log.get('device', 'unknown')
        error_type = log.get('error_type', 'unknown')
        device_errors[device][error_type] += 1
    
    logger.info(f"Counted errors for {len(device_errors)} devices")
    return dict(device_errors)


# ============================================================================
# Example 8: Interface Statistics Aggregation
# ============================================================================

def aggregate_interface_statistics(interfaces: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregate interface statistics by VLAN.
    
    Uses defaultdict to group without key checks.
    
    Args:
        interfaces: List of interface dictionaries
        
    Returns:
        Dictionary with aggregated statistics by VLAN
    """
    vlan_stats = defaultdict(lambda: {'count': 0, 'total_bandwidth': 0, 'interfaces': []})
    
    for interface in interfaces:
        vlan = interface.get('vlan', 'untagged')
        vlan_stats[vlan]['count'] += 1
        vlan_stats[vlan]['total_bandwidth'] += interface.get('bandwidth_mbps', 0)
        vlan_stats[vlan]['interfaces'].append(interface.get('name'))
    
    # Convert defaultdict to regular dict and calculate averages
    result = {}
    for vlan, stats in vlan_stats.items():
        count = stats['count']
        result[vlan] = {
            'interface_count': count,
            'total_bandwidth_mbps': stats['total_bandwidth'],
            'avg_bandwidth_mbps': stats['total_bandwidth'] / count if count > 0 else 0,
            'interfaces': stats['interfaces']
        }
    
    logger.info(f"Aggregated statistics for {len(result)} VLANs")
    return result


# ============================================================================
# Example 9: Recent Events Window
# ============================================================================

class RecentEventsWindow:
    """Maintain a sliding window of recent events."""
    
    def __init__(self, window_size: int = 100):
        """
        Initialize event window.
        
        Args:
            window_size: Maximum number of events to keep
        """
        self.events = deque(maxlen=window_size)
        self.window_size = window_size
    
    def add_event(self, event_type: str, device: str, message: str) -> None:
        """
        Add event to window.
        
        Args:
            event_type: Type of event (e.g., 'alert', 'info')
            device: Device name
            message: Event message
        """
        event = {
            'timestamp': datetime.now(),
            'type': event_type,
            'device': device,
            'message': message
        }
        self.events.append(event)
    
    def get_recent_by_type(self, event_type: str, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent events of specific type.
        
        Args:
            event_type: Type of events to retrieve
            count: Maximum number to return
            
        Returns:
            List of recent events
        """
        filtered = [e for e in self.events if e['type'] == event_type]
        return filtered[-count:]
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all events in window."""
        return list(self.events)


# ============================================================================
# Demonstration
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DATA STRUCTURES EXAMPLES")
    print("=" * 70)
    
    # Example 1: Grouping devices
    print("\n1. Grouping Devices by Vendor")
    devices = [
        {'hostname': 'r1', 'vendor': 'cisco', 'model': 'ASR1000'},
        {'hostname': 'r2', 'vendor': 'juniper', 'model': 'MX240'},
        {'hostname': 'r3', 'vendor': 'cisco', 'model': 'ISR4000'}
    ]
    grouped = group_devices_by_attribute(devices, 'vendor')
    print(f"Cisco devices: {len(grouped.get('cisco', []))}")
    print(f"Juniper devices: {len(grouped.get('juniper', []))}")
    
    # Example 2: Device facts
    print("\n2. Device Facts with namedtuple")
    device_data = {
        'hostname': 'router1',
        'vendor': 'cisco',
        'model': 'ASR1000',
        'os_version': '15.1',
        'serial_number': 'ABC123',
        'uptime_seconds': 86400
    }
    facts = create_device_facts(device_data)
    print(f"Hostname: {facts.hostname}, Vendor: {facts.vendor}")
    
    # Example 3: Interface status counting
    print("\n3. Interface Status Counting")
    interfaces = [
        {'name': 'Eth0', 'status': 'up'},
        {'name': 'Eth1', 'status': 'up'},
        {'name': 'Eth2', 'status': 'down'},
        {'name': 'Eth3', 'status': 'up'}
    ]
    analysis = analyze_interface_statuses(interfaces)
    print(f"Up: {analysis['up_count']}, Down: {analysis['down_count']}")
    
    # Example 4: Telemetry buffer
    print("\n4. Telemetry Buffer")
    buffer = TelemetryBuffer(max_size=5)
    buffer.add(datetime.now(), 'cpu', 45.5)
    buffer.add(datetime.now(), 'memory', 60.2)
    print(f"Buffer size: {buffer.size()}")
    
    # Example 5: Config order
    print("\n5. Configuration Order")
    steps = [
        {'name': 'step1', 'command': 'configure interface'},
        {'name': 'step2', 'command': 'configure routing'}
    ]
    plan = create_configuration_plan(steps)
    print(f"Steps in order: {list(plan.keys())}")
    
    # Example 6: Config duplication
    print("\n6. Config Duplication")
    original = {'device': 'r1', 'config': {'interface': 'Eth0'}}
    deep_copy = duplicate_device_config(original, deep=True)
    deep_copy['config']['interface'] = 'Eth1'
    print(f"Original unchanged: {original['config']['interface']}")
    
    # Example 7: Error counting
    print("\n7. Error Counting by Device")
    logs = [
        {'device': 'r1', 'error_type': 'timeout'},
        {'device': 'r1', 'error_type': 'timeout'},
        {'device': 'r2', 'error_type': 'connection'}
    ]
    error_counts = count_errors_by_device_and_type(logs)
    print(f"r1 errors: {dict(error_counts.get('r1', Counter()))}")
    
    # Example 8: Interface aggregation
    print("\n8. Interface Statistics Aggregation")
    interfaces = [
        {'name': 'Eth0', 'vlan': 100, 'bandwidth_mbps': 1000},
        {'name': 'Eth1', 'vlan': 100, 'bandwidth_mbps': 1000},
        {'name': 'Eth2', 'vlan': 200, 'bandwidth_mbps': 100}
    ]
    stats = aggregate_interface_statistics(interfaces)
    print(f"VLAN 100: {stats.get('100', {})}")
    
    # Example 9: Recent events
    print("\n9. Recent Events Window")
    window = RecentEventsWindow(window_size=10)
    window.add_event('alert', 'r1', 'High CPU')
    window.add_event('info', 'r2', 'Config updated')
    print(f"Total events: {len(window.get_all())}")
