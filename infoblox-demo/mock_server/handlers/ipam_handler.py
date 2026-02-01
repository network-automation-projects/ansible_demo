"""IPAM endpoint handlers for mock Infoblox server."""

from flask import request, jsonify
from mock_server.data_store import DataStore


def register_ipam_routes(app, data_store: DataStore):
    """Register IPAM-related routes.

    Args:
        app: Flask application
        data_store: Data store instance
    """

    @app.route("/wapi/v2.12/network", methods=["GET"])
    def get_ipam_networks():
        """GET /wapi/v2.12/network - List IPAM networks."""
        filters = {}
        if request.args.get("network"):
            filters["network"] = request.args.get("network")

        networks = data_store.get_ipam_networks(filters)
        return jsonify(networks)

    @app.route("/wapi/v2.12/network", methods=["POST"])
    def create_ipam_network():
        """POST /wapi/v2.12/network - Create IPAM network."""
        data = request.get_json()
        if not data.get("network"):
            return jsonify({"error": "network required"}), 400

        network = {
            "network": data["network"],
            "comment": data.get("comment"),
        }
        result = data_store.add_ipam_network(network)
        return jsonify(result), 201

    @app.route("/wapi/v2.12/ipv4address", methods=["GET"])
    def get_ip_addresses():
        """GET /wapi/v2.12/ipv4address - Get IP address information."""
        ip = request.args.get("ip_address")
        if ip:
            status = data_store.get_ip_status(ip)
            if status:
                return jsonify([status])
            return jsonify([])
        return jsonify([])

    @app.route("/wapi/v2.12/ipv4address", methods=["POST"])
    def allocate_ip():
        """POST /wapi/v2.12/ipv4address - Allocate IP address."""
        data = request.get_json()
        if not data.get("ip_address") or not data.get("network"):
            return jsonify({"error": "ip_address and network required"}), 400

        allocation = data_store.allocate_ip(
            data["network"], data["ip_address"], data.get("names", [None])[0] if data.get("names") else None
        )
        return jsonify(allocation), 201

    @app.route("/wapi/v2.12/request", methods=["POST"])
    def request_next_ip():
        """POST /wapi/v2.12/request - Request next available IP."""
        data = request.get_json()
        if not data.get("network"):
            return jsonify({"error": "network required"}), 400

        next_ip = data_store.get_next_available_ip(data["network"])
        if next_ip:
            return jsonify({"ipv4addr": next_ip}), 200
        return jsonify({"error": "No available IPs"}), 404
