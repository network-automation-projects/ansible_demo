"""Mock Infoblox WAPI server for learning and testing."""

import logging
from flask import Flask, jsonify
from mock_server.data_store import DataStore
from mock_server.handlers import dns_handler, dhcp_handler, ipam_handler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
data_store = DataStore()

# Initialize data store
data_store.load_sample_data()
logger.info("Mock Infoblox server initialized with sample data")


@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "Mock Infoblox WAPI"})


@app.route("/wapi/v2.12", methods=["GET"])
def wapi_info():
    """WAPI info endpoint."""
    return jsonify({"version": "2.12", "type": "mock"})


# Register all route handlers
dns_handler.register_dns_routes(app, data_store)
dhcp_handler.register_dhcp_routes(app, data_store)
ipam_handler.register_ipam_routes(app, data_store)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal error: {error}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    logger.info("Starting Mock Infoblox WAPI server on http://localhost:8080")
    app.run(host="0.0.0.0", port=8080, debug=True)
