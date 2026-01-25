"""
utils/database.py

SQLite database operations for device inventory, backups, and audit results.

LEARNING NOTES:
This module manages all database operations using SQLite.
SQLite is a file-based database that doesn't require a separate server.

KEY CONCEPTS:
1. SQLite connection - file-based database stored in data/inventory.db
2. Table creation - devices, backups, audit_results tables
3. CRUD operations - Create, Read, Update, Delete
4. JSON storage - device facts stored as JSON strings
5. Context manager - use 'with Database()' for automatic cleanup

DATABASE SCHEMA:
- devices: ip (PK), hostname, device_type, status, last_seen, facts_json, created_at, updated_at
- backups: id (PK), device_ip (FK), backup_path, timestamp, size_bytes, created_at
- audit_results: id (PK), device_ip (FK), check_name, status, details, timestamp, created_at

IMPLEMENTATION ORDER:
1. Start with __init__ and _create_tables()
2. Then implement upsert_device() and get_device()
3. Then get_all_devices()
4. Then backup-related methods (add_backup, get_backups)
5. Then audit-related methods
6. Finally get_device_stats()
"""

import os
import sqlite3
# TODO: Uncomment when ready to use
# import json
import logging
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class Database:
    """
    Database manager for network device inventory and backups.
    
    This class handles all database operations for the dashboard.
    It uses SQLite which stores data in a single file (data/inventory.db).
    """

    def __init__(self, db_path: str = "data/inventory.db"):
        """
        Initialize database connection and create tables if needed.
        
        TODO: Implement this method to:
        1. Create the data directory if it doesn't exist (os.makedirs with exist_ok=True)
        2. Store db_path as instance variable
        3. Create SQLite connection: sqlite3.connect(db_path, check_same_thread=False)
        4. Set row_factory to sqlite3.Row (enables column access by name)
        5. Call self._create_tables() to initialize schema
        
        Parameters:
        - db_path: Path to SQLite database file (default: "data/inventory.db")
        """
        # TODO: Create directory and connect to database
        # os.makedirs(os.path.dirname(db_path), exist_ok=True)
        # self.db_path = db_path
        # self.conn = sqlite3.connect(db_path, check_same_thread=False)
        # self.conn.row_factory = sqlite3.Row  # Enable column access by name
        # self._create_tables()
        
        self.db_path = db_path
        self.conn = None
        logger.warning("Database.__init__() not yet implemented")

    def _create_tables(self):
        """
        Create database tables if they don't exist.
        
        TODO: Implement this method to create three tables:
        
        1. devices table:
           - ip TEXT PRIMARY KEY
           - hostname TEXT
           - device_type TEXT
           - status TEXT
           - last_seen TEXT
           - facts_json TEXT (stores JSON string of device facts)
           - created_at TEXT DEFAULT CURRENT_TIMESTAMP
           - updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        
        2. backups table:
           - id INTEGER PRIMARY KEY AUTOINCREMENT
           - device_ip TEXT (foreign key to devices.ip)
           - backup_path TEXT
           - timestamp TEXT
           - size_bytes INTEGER
           - created_at TEXT DEFAULT CURRENT_TIMESTAMP
           - FOREIGN KEY (device_ip) REFERENCES devices(ip)
        
        3. audit_results table:
           - id INTEGER PRIMARY KEY AUTOINCREMENT
           - device_ip TEXT (foreign key to devices.ip)
           - check_name TEXT
           - status TEXT
           - details TEXT
           - timestamp TEXT
           - created_at TEXT DEFAULT CURRENT_TIMESTAMP
           - FOREIGN KEY (device_ip) REFERENCES devices(ip)
        
        Use cursor.execute() with CREATE TABLE IF NOT EXISTS statements.
        Call self.conn.commit() after creating tables.
        """
        # TODO: Create tables
        # cursor = self.conn.cursor()
        # 
        # # Devices table
        # cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS devices (
        #         ip TEXT PRIMARY KEY,
        #         hostname TEXT,
        #         device_type TEXT,
        #         status TEXT,
        #         last_seen TEXT,
        #         facts_json TEXT,
        #         created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        #         updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        #     )
        # """)
        # 
        # # Backups table
        # cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS backups (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         device_ip TEXT,
        #         backup_path TEXT,
        #         timestamp TEXT,
        #         size_bytes INTEGER,
        #         created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        #         FOREIGN KEY (device_ip) REFERENCES devices(ip)
        #     )
        # """)
        # 
        # # Audit results table
        # cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS audit_results (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         device_ip TEXT,
        #         check_name TEXT,
        #         status TEXT,
        #         details TEXT,
        #         timestamp TEXT,
        #         created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        #         FOREIGN KEY (device_ip) REFERENCES devices(ip)
        #     )
        # """)
        # 
        # self.conn.commit()
        # logger.info("Database tables initialized")
        
        logger.warning("_create_tables() not yet implemented")

    def upsert_device(self, device: Dict) -> bool:
        """
        Insert or update device information.
        Returns True on success, False on error.
        
        TODO: Implement this method to:
        1. Convert device['facts'] dict to JSON string using json.dumps() if facts exist
        2. Get current timestamp using datetime.now().isoformat()
        3. Use INSERT OR REPLACE to update existing device or insert new one
        4. Execute SQL with parameters: ip, hostname, device_type, status, last_seen, facts_json, updated_at
        5. Commit the transaction
        6. Return True on success, False on exception
        
        Parameters:
        - device: Dictionary with keys: ip, hostname, device_type, status, facts (optional)
        
        Returns:
        bool: True if successful, False otherwise
        """
        try:
            # TODO: Implement upsert logic
            # cursor = self.conn.cursor()
            # facts_json = json.dumps(device.get('facts', {})) if device.get('facts') else None
            # now = datetime.now().isoformat()
            # 
            # cursor.execute("""
            #     INSERT OR REPLACE INTO devices 
            #     (ip, hostname, device_type, status, last_seen, facts_json, updated_at)
            #     VALUES (?, ?, ?, ?, ?, ?, ?)
            # """, (
            #     device['ip'],
            #     device.get('hostname', ''),
            #     device.get('device_type', ''),
            #     device.get('status', 'unknown'),
            #     now,
            #     facts_json,
            #     now
            # ))
            # 
            # self.conn.commit()
            # logger.debug(f"Upserted device {device['ip']}")
            # return True
            
            logger.warning(f"upsert_device() not yet implemented for {device.get('ip', 'unknown')}")
            return False
        except Exception as e:
            logger.error(f"Failed to upsert device {device.get('ip', 'unknown')}: {e}")
            return False

    def get_device(self, ip: str) -> Optional[Dict]:
        """
        Get device information by IP address.
        
        TODO: Implement this method to:
        1. Execute SELECT query: SELECT * FROM devices WHERE ip = ?
        2. Fetch one row using cursor.fetchone()
        3. If row exists, convert to dict using dict(row)
        4. If facts_json exists, parse it using json.loads() and store in 'facts' key
        5. Remove 'facts_json' key after parsing
        6. Return device dict, or None if not found
        
        Parameters:
        - ip: IP address of the device
        
        Returns:
        Optional[Dict]: Device dictionary or None if not found
        """
        try:
            # TODO: Implement get device logic
            # cursor = self.conn.cursor()
            # cursor.execute("SELECT * FROM devices WHERE ip = ?", (ip,))
            # row = cursor.fetchone()
            # if row:
            #     device = dict(row)
            #     if device.get('facts_json'):
            #         device['facts'] = json.loads(device['facts_json'])
            #     return device
            # return None
            
            logger.warning(f"get_device() not yet implemented for {ip}")
            return None
        except Exception as e:
            logger.error(f"Failed to get device {ip}: {e}")
            return None

    def get_all_devices(self) -> List[Dict]:
        """
        Get all devices from database.
        
        TODO: Implement this method to:
        1. Execute SELECT query: SELECT * FROM devices ORDER BY hostname, ip
        2. Fetch all rows using cursor.fetchall()
        3. Convert each row to dict
        4. Parse facts_json to facts for each device
        5. Return list of device dictionaries
        
        Returns:
        List[Dict]: List of all device dictionaries
        """
        try:
            # TODO: Implement get all devices logic
            # cursor = self.conn.cursor()
            # cursor.execute("SELECT * FROM devices ORDER BY hostname, ip")
            # rows = cursor.fetchall()
            # devices = []
            # for row in rows:
            #     device = dict(row)
            #     if device.get('facts_json'):
            #         device['facts'] = json.loads(device['facts_json'])
            #     devices.append(device)
            # return devices
            
            logger.warning("get_all_devices() not yet implemented")
            return []
        except Exception as e:
            logger.error(f"Failed to get all devices: {e}")
            return []

    def add_backup(self, device_ip: str, backup_path: str, size_bytes: int) -> bool:
        """
        Add backup record to database.
        
        TODO: Implement this method to:
        1. Get current timestamp using datetime.now().isoformat()
        2. Execute INSERT query into backups table
        3. Parameters: device_ip, backup_path, timestamp, size_bytes
        4. Commit transaction
        5. Return True on success, False on exception
        
        Parameters:
        - device_ip: IP address of the device
        - backup_path: Path to the backup file
        - size_bytes: Size of the backup file in bytes
        
        Returns:
        bool: True if successful, False otherwise
        """
        try:
            # TODO: Implement add backup logic
            # cursor = self.conn.cursor()
            # timestamp = datetime.now().isoformat()
            # cursor.execute("""
            #     INSERT INTO backups (device_ip, backup_path, timestamp, size_bytes)
            #     VALUES (?, ?, ?, ?)
            # """, (device_ip, backup_path, timestamp, size_bytes))
            # self.conn.commit()
            # logger.debug(f"Added backup record for {device_ip}")
            # return True
            
            logger.warning(f"add_backup() not yet implemented for {device_ip}")
            return False
        except Exception as e:
            logger.error(f"Failed to add backup record: {e}")
            return False

    def get_backups(self, device_ip: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """
        Get backup records, optionally filtered by device IP.
        
        TODO: Implement this method to:
        1. If device_ip is provided, query: SELECT * FROM backups WHERE device_ip = ? ORDER BY timestamp DESC LIMIT ?
        2. If device_ip is None, query: SELECT * FROM backups ORDER BY timestamp DESC LIMIT ?
        3. Fetch all rows and convert to list of dicts
        4. Return list of backup dictionaries
        
        Parameters:
        - device_ip: Optional IP address to filter by
        - limit: Maximum number of records to return (default: 50)
        
        Returns:
        List[Dict]: List of backup dictionaries
        """
        try:
            # TODO: Implement get backups logic
            # cursor = self.conn.cursor()
            # if device_ip:
            #     cursor.execute("""
            #         SELECT * FROM backups 
            #         WHERE device_ip = ? 
            #         ORDER BY timestamp DESC 
            #         LIMIT ?
            #     """, (device_ip, limit))
            # else:
            #     cursor.execute("""
            #         SELECT * FROM backups 
            #         ORDER BY timestamp DESC 
            #         LIMIT ?
            #     """, (limit,))
            # rows = cursor.fetchall()
            # return [dict(row) for row in rows]
            
            logger.warning("get_backups() not yet implemented")
            return []
        except Exception as e:
            logger.error(f"Failed to get backups: {e}")
            return []

    def add_audit_result(self, device_ip: str, check_name: str, status: str, details: str) -> bool:
        """
        Add audit result to database.
        
        TODO: Implement this method to:
        1. Get current timestamp
        2. Execute INSERT query into audit_results table
        3. Parameters: device_ip, check_name, status, details, timestamp
        4. Commit and return True/False
        
        Parameters:
        - device_ip: IP address of the device
        - check_name: Name of the audit check
        - status: Status of the check (e.g., 'pass', 'fail')
        - details: Details about the audit result
        
        Returns:
        bool: True if successful, False otherwise
        """
        try:
            # TODO: Implement add audit result logic
            # cursor = self.conn.cursor()
            # timestamp = datetime.now().isoformat()
            # cursor.execute("""
            #     INSERT INTO audit_results (device_ip, check_name, status, details, timestamp)
            #     VALUES (?, ?, ?, ?, ?)
            # """, (device_ip, check_name, status, details, timestamp))
            # self.conn.commit()
            # logger.debug(f"Added audit result for {device_ip}")
            # return True
            
            logger.warning(f"add_audit_result() not yet implemented for {device_ip}")
            return False
        except Exception as e:
            logger.error(f"Failed to add audit result: {e}")
            return False

    def get_audit_results(self, device_ip: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """
        Get audit results, optionally filtered by device IP.
        
        TODO: Implement similar to get_backups() but for audit_results table.
        
        Parameters:
        - device_ip: Optional IP address to filter by
        - limit: Maximum number of records to return (default: 100)
        
        Returns:
        List[Dict]: List of audit result dictionaries
        """
        try:
            # TODO: Implement get audit results logic
            logger.warning("get_audit_results() not yet implemented")
            return []
        except Exception as e:
            logger.error(f"Failed to get audit results: {e}")
            return []

    def get_device_stats(self) -> Dict:
        """
        Get summary statistics about devices.
        
        TODO: Implement this method to calculate:
        1. Total device count: SELECT COUNT(*) FROM devices
        2. Devices by status: SELECT status, COUNT(*) FROM devices GROUP BY status
        3. Total backups: SELECT COUNT(*) FROM backups
        4. Recent backups (last 24 hours): SELECT COUNT(*) FROM backups WHERE timestamp > datetime('now', '-1 day')
        5. Return dict with keys: 'total', 'by_status', 'total_backups', 'recent_backups'
        
        Returns:
        Dict: Statistics dictionary
        Example:
        {
            'total': 10,
            'by_status': {'reachable': 8, 'unreachable': 2},
            'total_backups': 45,
            'recent_backups': 5
        }
        """
        try:
            # TODO: Implement get stats logic
            # cursor = self.conn.cursor()
            # stats = {}
            # 
            # # Total devices
            # cursor.execute("SELECT COUNT(*) as count FROM devices")
            # stats['total'] = cursor.fetchone()['count']
            # 
            # # Devices by status
            # cursor.execute("""
            #     SELECT status, COUNT(*) as count 
            #     FROM devices 
            #     GROUP BY status
            # """)
            # stats['by_status'] = {row['status']: row['count'] for row in cursor.fetchall()}
            # 
            # # Total backups
            # cursor.execute("SELECT COUNT(*) as count FROM backups")
            # stats['total_backups'] = cursor.fetchone()['count']
            # 
            # # Recent backups
            # cursor.execute("""
            #     SELECT COUNT(*) as count 
            #     FROM backups 
            #     WHERE timestamp > datetime('now', '-1 day')
            # """)
            # stats['recent_backups'] = cursor.fetchone()['count']
            # 
            # return stats
            
            logger.warning("get_device_stats() not yet implemented")
            return {}
        except Exception as e:
            logger.error(f"Failed to get device stats: {e}")
            return {}

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()



