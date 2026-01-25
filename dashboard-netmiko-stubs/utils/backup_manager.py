"""
utils/backup_manager.py

Configuration backup functionality with database integration.

LEARNING NOTES:
This module orchestrates configuration backups by combining:
- Netmiko connections (from core.netmiko_core)
- Database operations (from utils.database)
- File system operations (writing backup files)

KEY CONCEPTS:
1. Integration - combines multiple modules to accomplish a task
2. Backup lifecycle - backup, store, track, cleanup
3. Error handling - backups can fail for many reasons
4. Database tracking - record backups in database for history

IMPLEMENTATION ORDER:
1. Implement __init__() to initialize backup directory and database
2. Implement backup_device() for single device backup
3. Implement backup_device_by_ip() to find device and backup
4. Implement backup_all_devices() for batch operations
5. Implement get_backup_history() and get_latest_backup()
6. Finally implement cleanup_old_backups() for maintenance
"""

import os
import logging
from typing import Optional, List, Dict
from datetime import datetime

# TODO: Uncomment when ready to use
# from core.netmiko_core import backup_config, load_inventory, get_credentials
# from utils.database import Database

logger = logging.getLogger(__name__)


class BackupManager:
    """
    Manages configuration backups for network devices.
    
    This class coordinates between Netmiko (for device connections),
    the file system (for storing backups), and the database (for tracking).
    """

    def __init__(self, backup_dir: str = "backups", db: Optional['Database'] = None):
        """
        Initialize backup manager.
        
        TODO: Implement this method to:
        1. Store backup_dir as instance variable
        2. Create backup directory if it doesn't exist (os.makedirs with exist_ok=True)
        3. Store database instance (use provided db or create new Database() if None)
        
        Parameters:
        - backup_dir: Directory where backups will be stored (default: "backups")
        - db: Database instance (optional, creates new one if not provided)
        """
        # TODO: Initialize backup directory and database
        # self.backup_dir = backup_dir
        # os.makedirs(backup_dir, exist_ok=True)
        # self.db = db or Database()
        
        self.backup_dir = backup_dir
        self.db = None
        logger.warning("BackupManager.__init__() not yet implemented")

    def backup_device(self, device: Dict) -> Optional[str]:
        """
        Backup configuration for a single device.
        Returns backup file path on success, None on failure.
        
        TODO: Implement this method to:
        1. Call backup_config(device, self.backup_dir) from netmiko_core
        2. If backup_path is returned and file exists:
           a. Get file size using os.path.getsize(backup_path)
           b. Record backup in database using self.db.add_backup()
           c. Log success and return backup_path
        3. If backup failed, log warning and return None
        4. Handle exceptions and return None on error
        
        Parameters:
        - device: Device dictionary with ip, hostname, device_type, etc.
        
        Returns:
        Optional[str]: Path to backup file, or None if backup failed
        """
        try:
            # TODO: Implement backup logic
            # backup_path = backup_config(device, self.backup_dir)
            # if backup_path and os.path.exists(backup_path):
            #     size_bytes = os.path.getsize(backup_path)
            #     self.db.add_backup(device['ip'], backup_path, size_bytes)
            #     logger.info(f"Backup completed for {device['ip']}: {backup_path}")
            #     return backup_path
            # else:
            #     logger.warning(f"Backup failed for {device['ip']}")
            #     return None
            
            logger.warning(f"backup_device() not yet implemented for {device.get('ip', 'unknown')}")
            return None
        except Exception as e:
            logger.error(f"Error backing up {device['ip']}: {e}")
            return None

    def backup_device_by_ip(self, ip: str, inventory_file: str = "config/devices.yaml") -> Optional[str]:
        """
        Backup device by IP address.
        
        TODO: Implement this method to:
        1. Load inventory using load_inventory(inventory_file)
        2. Find device with matching IP using next() with generator expression
        3. If device found, call self.backup_device(device)
        4. If device not found, log error and return None
        
        Parameters:
        - ip: IP address of the device to backup
        - inventory_file: Path to inventory YAML file
        
        Returns:
        Optional[str]: Path to backup file, or None if backup failed
        """
        # TODO: Load inventory and find device
        # devices = load_inventory(inventory_file)
        # device = next((d for d in devices if d['ip'] == ip), None)
        # if device:
        #     return self.backup_device(device)
        # else:
        #     logger.error(f"Device with IP {ip} not found in inventory")
        #     return None
        
        logger.warning(f"backup_device_by_ip() not yet implemented for {ip}")
        return None

    def backup_all_devices(self, inventory_file: str = "config/devices.yaml") -> Dict[str, Optional[str]]:
        """
        Backup all devices in inventory.
        Returns dictionary mapping device IPs to backup paths.
        
        TODO: Implement this method to:
        1. Load inventory using load_inventory(inventory_file)
        2. Loop through each device
        3. Call self.backup_device(device) for each
        4. Store result in results dict: results[device['ip']] = backup_path
        5. Return results dictionary
        
        Parameters:
        - inventory_file: Path to inventory YAML file
        
        Returns:
        Dict[str, Optional[str]]: Dictionary mapping IP addresses to backup paths
        Example: {'192.168.1.1': '/path/to/backup.cfg', '192.168.1.2': None}
        """
        # TODO: Implement backup all devices logic
        # devices = load_inventory(inventory_file)
        # results = {}
        # for device in devices:
        #     backup_path = self.backup_device(device)
        #     results[device['ip']] = backup_path
        # return results
        
        logger.warning("backup_all_devices() not yet implemented")
        return {}

    def get_backup_history(self, device_ip: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """
        Get backup history from database.
        
        TODO: Implement this method to:
        1. Call self.db.get_backups(device_ip, limit)
        2. Return the list of backup records
        
        Parameters:
        - device_ip: Optional IP address to filter by
        - limit: Maximum number of records to return
        
        Returns:
        List[Dict]: List of backup dictionaries
        """
        # TODO: Implement get backup history
        # return self.db.get_backups(device_ip, limit)
        
        logger.warning("get_backup_history() not yet implemented")
        return []

    def get_latest_backup(self, device_ip: str) -> Optional[Dict]:
        """
        Get the most recent backup for a device.
        
        TODO: Implement this method to:
        1. Get backups using self.db.get_backups(device_ip, limit=1)
        2. Return first backup if list is not empty, else None
        
        Parameters:
        - device_ip: IP address of the device
        
        Returns:
        Optional[Dict]: Most recent backup dictionary, or None if no backups
        """
        # TODO: Implement get latest backup
        # backups = self.db.get_backups(device_ip, limit=1)
        # return backups[0] if backups else None
        
        logger.warning(f"get_latest_backup() not yet implemented for {device_ip}")
        return None

    def cleanup_old_backups(self, days: int = 30, keep_latest: int = 5) -> int:
        """
        Remove backup files older than specified days, but keep at least
        the N most recent backups per device.
        Returns number of files deleted.
        
        TODO: Implement this method to:
        1. Calculate cutoff_date = datetime.now() - timedelta(days=days)
        2. Get all backups from database (use large limit like 10000)
        3. Group backups by device_ip into a dictionary
        4. For each device:
           a. Sort backups by timestamp (newest first)
           b. Keep the first 'keep_latest' backups
           c. For remaining backups, check if timestamp < cutoff_date
           d. If old enough, delete file using os.remove()
           e. Count deleted files
        5. Return total count of deleted files
        
        This is a maintenance function to prevent backup directory from growing too large.
        
        Parameters:
        - days: Number of days to keep backups (default: 30)
        - keep_latest: Minimum number of recent backups to keep per device (default: 5)
        
        Returns:
        int: Number of backup files deleted
        """
        # TODO: Implement cleanup logic
        # from datetime import timedelta
        # cutoff_date = datetime.now() - timedelta(days=days)
        # deleted_count = 0
        # 
        # try:
        #     all_backups = self.db.get_backups(limit=10000)
        #     backups_by_device: Dict[str, List[Dict]] = {}
        #     for backup in all_backups:
        #         device_ip = backup['device_ip']
        #         if device_ip not in backups_by_device:
        #             backups_by_device[device_ip] = []
        #         backups_by_device[device_ip].append(backup)
        # 
        #     for device_ip, backups in backups_by_device.items():
        #         backups.sort(key=lambda x: x['timestamp'], reverse=True)
        #         to_keep = backups[:keep_latest]
        #         to_check = backups[keep_latest:]
        #         
        #         for backup in to_check:
        #             backup_timestamp = datetime.fromisoformat(backup['timestamp'])
        #             if backup_timestamp < cutoff_date:
        #                 backup_path = backup['backup_path']
        #                 if os.path.exists(backup_path):
        #                     try:
        #                         os.remove(backup_path)
        #                         deleted_count += 1
        #                         logger.info(f"Deleted old backup: {backup_path}")
        #                     except Exception as e:
        #                         logger.error(f"Failed to delete {backup_path}: {e}")
        # 
        #     logger.info(f"Cleanup completed: {deleted_count} old backups removed")
        #     return deleted_count
        # except Exception as e:
        #     logger.error(f"Error during backup cleanup: {e}")
        #     return deleted_count
        
        logger.warning("cleanup_old_backups() not yet implemented")
        return 0



