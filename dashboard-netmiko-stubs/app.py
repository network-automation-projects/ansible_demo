"""
app.py

Flask web application for Network Automation Dashboard.

LEARNING NOTES:
This is the main Flask application file. It ties together:
- Routes (URL endpoints) that users can visit
- Templates (HTML pages) that get rendered
- Database operations (stored in utils/database.py)
- Backup operations (stored in utils/backup_manager.py)
- Device facts collection (stored in core/netmiko_core.py)

IMPLEMENTATION ORDER SUGGESTION:
1. Start with core/netmiko_core.py to understand device connections
2. Then implement utils/database.py for data storage
3. Then utils/backup_manager.py for backup functionality
4. Finally, implement the routes in this file
"""

import os
import logging
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from datetime import datetime

# TODO: Uncomment these imports once you've implemented the modules
# from core.netmiko_core import collect_all_facts, load_inventory
# from utils.database import Database
# from utils.backup_manager import BackupManager

# Configure logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# TODO: Initialize database and backup manager
# db = Database()
# backup_mgr = BackupManager(db=db)

# For now, use placeholder objects
db = None
backup_mgr = None


@app.route('/')
def index():
    """
    Dashboard home page with device status overview.
    
    TODO: Implement this route to:
    1. Get device statistics from the database (db.get_device_stats())
    2. Get all devices from the database (db.get_all_devices())
    3. Get recent backups (db.get_backups(limit=10))
    4. Pass these to the template: render_template('index.html', stats=stats, devices=devices, recent_backups=recent_backups)
    5. Handle errors gracefully with try/except and flash messages
    
    Expected return format:
    - stats: dict with keys like 'total', 'by_status', 'total_backups', 'recent_backups'
    - devices: list of device dictionaries
    - recent_backups: list of backup dictionaries
    """
    try:
        # TODO: Replace these placeholder values with actual database calls
        stats = {}  # Should be: db.get_device_stats()
        devices = []  # Should be: db.get_all_devices()
        recent_backups = []  # Should be: db.get_backups(limit=10)
        
        return render_template('index.html', 
                             stats=stats, 
                             devices=devices, 
                             recent_backups=recent_backups)
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        flash(f"Error loading dashboard: {e}", "error")
        return render_template('index.html', stats={}, devices=[], recent_backups=[])


@app.route('/devices')
def devices():
    """
    List all devices with status indicators.
    
    TODO: Implement this route to:
    1. Get all devices from database (db.get_all_devices())
    2. Pass to template: render_template('devices.html', devices=devices)
    3. Handle errors with try/except
    
    The template expects a list of device dictionaries with keys like:
    - ip, hostname, device_type, status, last_seen, facts, error
    """
    try:
        # TODO: Replace with actual database call
        devices = []  # Should be: db.get_all_devices()
        return render_template('devices.html', devices=devices)
    except Exception as e:
        logger.error(f"Error in devices route: {e}")
        flash(f"Error loading devices: {e}", "error")
        return render_template('devices.html', devices=[])


@app.route('/device/<ip>')
def device_detail(ip):
    """
    Device detail page with facts and recent backups.
    
    TODO: Implement this route to:
    1. Get device by IP from database (db.get_device(ip))
    2. If device not found, flash error and redirect to devices page
    3. Get backups for this device (db.get_backups(device_ip=ip, limit=20))
    4. Get audit results (db.get_audit_results(device_ip=ip, limit=20))
    5. Pass to template: render_template('device_detail.html', device=device, backups=backups, audit_results=audit_results)
    
    Parameters:
    - ip: IP address of the device (from URL)
    """
    try:
        # TODO: Replace with actual database calls
        device = None  # Should be: db.get_device(ip)
        if not device:
            flash(f"Device {ip} not found", "error")
            return redirect(url_for('devices'))
        
        backups = []  # Should be: db.get_backups(device_ip=ip, limit=20)
        audit_results = []  # Should be: db.get_audit_results(device_ip=ip, limit=20)
        
        return render_template('device_detail.html', 
                             device=device, 
                             backups=backups,
                             audit_results=audit_results)
    except Exception as e:
        logger.error(f"Error in device_detail route: {e}")
        flash(f"Error loading device details: {e}", "error")
        return redirect(url_for('devices'))


@app.route('/backup/<ip>', methods=['POST'])
def trigger_backup(ip):
    """
    Trigger manual backup for a device.
    
    TODO: Implement this route to:
    1. Call backup_mgr.backup_device_by_ip(ip)
    2. If successful, flash success message with backup path
    3. If failed, flash error message
    4. Redirect back to device detail page
    
    This is a POST route, so it's called when a form is submitted.
    The template has a form that POSTs to this route.
    """
    try:
        # TODO: Replace with actual backup call
        backup_path = None  # Should be: backup_mgr.backup_device_by_ip(ip)
        if backup_path:
            flash(f"Backup completed successfully: {backup_path}", "success")
        else:
            flash(f"Backup failed for device {ip}", "error")
    except Exception as e:
        logger.error(f"Error triggering backup for {ip}: {e}")
        flash(f"Error during backup: {e}", "error")
    
    return redirect(url_for('device_detail', ip=ip))


@app.route('/refresh', methods=['POST'])
def refresh_devices():
    """
    Refresh all device facts (AJAX endpoint).
    
    TODO: Implement this route to:
    1. Call collect_all_facts(max_workers=10) to gather facts from all devices
    2. Update database with new facts: db.upsert_device(device) for each device
    3. Return JSON response: jsonify({'success': True, 'message': f'Refreshed {len(devices)} devices', 'count': len(devices)})
    4. Handle errors and return error JSON with 500 status
    
    This is called via AJAX from the frontend, so it returns JSON, not HTML.
    """
    try:
        # TODO: Replace with actual fact collection
        devices = []  # Should be: collect_all_facts(max_workers=10)
        
        # TODO: Update database with new facts
        # for device in devices:
        #     db.upsert_device(device)
        
        return jsonify({
            'success': True,
            'message': f'Refreshed {len(devices)} devices',
            'count': len(devices)
        })
    except Exception as e:
        logger.error(f"Error refreshing devices: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/devices')
def api_devices():
    """
    JSON API for device list.
    
    TODO: Implement this route to:
    1. Get all devices from database (db.get_all_devices())
    2. Convert to JSON-serializable format (remove facts_json if facts exists)
    3. Return jsonify(devices_json)
    4. Handle errors and return error JSON with 500 status
    
    This is a REST API endpoint that returns JSON data.
    Useful for programmatic access or AJAX calls from frontend.
    """
    try:
        # TODO: Replace with actual database call
        devices = []  # Should be: db.get_all_devices()
        
        # Convert to JSON-serializable format
        devices_json = []
        for device in devices:
            device_dict = dict(device)
            # Remove facts_json if facts exists
            if 'facts' in device_dict:
                device_dict.pop('facts_json', None)
            devices_json.append(device_dict)
        
        return jsonify(devices_json)
    except Exception as e:
        logger.error(f"Error in api_devices: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/device/<ip>/facts')
def api_device_facts(ip):
    """
    JSON API for device facts.
    
    TODO: Implement this route to:
    1. Get device by IP (db.get_device(ip))
    2. If not found, return 404 with error JSON
    3. Convert to JSON-serializable format
    4. Return jsonify(device_dict)
    """
    try:
        # TODO: Replace with actual database call
        device = None  # Should be: db.get_device(ip)
        if not device:
            return jsonify({'error': 'Device not found'}), 404
        
        device_dict = dict(device)
        if 'facts_json' in device_dict:
            device_dict.pop('facts_json', None)
        
        return jsonify(device_dict)
    except Exception as e:
        logger.error(f"Error in api_device_facts: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
def api_stats():
    """
    JSON API for dashboard statistics.
    
    TODO: Implement this route to:
    1. Get stats from database (db.get_device_stats())
    2. Return jsonify(stats)
    """
    try:
        # TODO: Replace with actual database call
        stats = {}  # Should be: db.get_device_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error in api_stats: {e}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('logs', exist_ok=True)
    os.makedirs('backups', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)



