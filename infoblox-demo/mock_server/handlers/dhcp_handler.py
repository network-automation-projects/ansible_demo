"""DHCP endpoint handlers for mock Infoblox server."""

from flask import request, jsonify
from mock_server.data_store import DataStore


def register_dhcp_routes(app, data_store: DataStore):
    """Register DHCP-related routes.

    Args:
        app: Flask application
        data_store: Data store instance
    """

    @app.route("/wapi/v2.12/network", methods=["GET"])
    def get_networks():
        """GET /wapi/v2.12/network - List DHCP networks."""
        filters = {}
        if request.args.get("network"):
            filters["network"] = request.args.get("network")

        networks = data_store.get_dhcp_networks(filters)
        return jsonify(networks)

    @app.route("/wapi/v2.12/network", methods=["POST"])
    def create_network():
        """POST /wapi/v2.12/network - Create DHCP network."""
        data = request.get_json()
        if not data.get("network"):
            return jsonify({"error": "network required"}), 400

        network = {
            "network": data["network"],
            "comment": data.get("comment"),
        }
        result = data_store.add_dhcp_network(network)
        return jsonify(result), 201

    @app.route("/wapi/v2.12/range", methods=["GET"])
    def get_ranges():
        """GET /wapi/v2.12/range - List DHCP ranges."""
        filters = {}
        if request.args.get("network"):
            filters["network"] = request.args.get("network")

        ranges = data_store.get_dhcp_ranges(filters)
        return jsonify(ranges)

    @app.route("/wapi/v2.12/range", methods=["POST"])
    def create_range():
        """POST /wapi/v2.12/range - Create DHCP range."""
        data = request.get_json()
        if not data.get("start_ip") or not data.get("end_ip") or not data.get("network"):
            return jsonify({"error": "start_ip, end_ip, and network required"}), 400

        range_obj = {
            "start_ip": data["start_ip"],
            "end_ip": data["end_ip"],
            "network": data["network"],
            "comment": data.get("comment"),
        }
        result = data_store.add_dhcp_range(range_obj)
        return jsonify(result), 201

    @app.route("/wapi/v2.12/fixedaddress", methods=["GET"])
    def get_reservations():
        """GET /wapi/v2.12/fixedaddress - List DHCP reservations."""
        filters = {}
        if request.args.get("ipv4addr"):
            filters["ipv4addr"] = request.args.get("ipv4addr")
        if request.args.get("mac"):
            filters["mac"] = request.args.get("mac")

        reservations = data_store.get_dhcp_reservations(filters)
        return jsonify(reservations)

    @app.route("/wapi/v2.12/fixedaddress", methods=["POST"])
    def create_reservation():
        """POST /wapi/v2.12/fixedaddress - Create DHCP reservation."""
        data = request.get_json()
        if not data.get("ipv4addr") or not data.get("mac"):
            return jsonify({"error": "ipv4addr and mac required"}), 400

        reservation = {
            "ipv4addr": data["ipv4addr"],
            "mac": data["mac"],
            "name": data.get("name"),
            "comment": data.get("comment"),
        }
        result = data_store.add_dhcp_reservation(reservation)
        return jsonify(result), 201
