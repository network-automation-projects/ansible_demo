"""DNS endpoint handlers for mock Infoblox server."""

from typing import Any, Dict, List
from flask import request, jsonify
from mock_server.data_store import DataStore


def register_dns_routes(app, data_store: DataStore):
    """Register DNS-related routes.

    Args:
        app: Flask application
        data_store: Data store instance
    """

    @app.route("/wapi/v2.12/record:a", methods=["GET"])
    def get_a_records():
        """GET /wapi/v2.12/record:a - List A records."""
        filters = {}
        if request.args.get("name"):
            filters["name"] = request.args.get("name")
        if request.args.get("ipv4addr"):
            filters["ipv4addr"] = request.args.get("ipv4addr")

        records = data_store.get_dns_records(
            {k: v for k, v in filters.items() if k in ["name", "ipv4addr"]}
        )
        # Filter to only A records
        a_records = [r for r in records if r.get("record_type", "A").upper() == "A"]
        return jsonify(a_records)

    @app.route("/wapi/v2.12/record:a", methods=["POST"])
    def create_a_record():
        """POST /wapi/v2.12/record:a - Create A record."""
        data = request.get_json()
        if not data.get("name") or not data.get("ipv4addr"):
            return jsonify({"error": "name and ipv4addr required"}), 400

        record = {
            "name": data["name"],
            "ipv4addr": data["ipv4addr"],
            "record_type": "A",
            "comment": data.get("comment"),
            "ttl": data.get("ttl"),
        }
        result = data_store.add_dns_record(record)
        return jsonify(result), 201

    @app.route("/wapi/v2.12/record:cname", methods=["GET"])
    def get_cname_records():
        """GET /wapi/v2.12/record:cname - List CNAME records."""
        filters = {}
        if request.args.get("name"):
            filters["name"] = request.args.get("name")
        if request.args.get("canonical"):
            filters["canonical"] = request.args.get("canonical")

        records = data_store.get_dns_records(filters)
        # Filter to only CNAME records
        cname_records = [
            r for r in records if r.get("record_type", "").upper() == "CNAME"
        ]
        return jsonify(cname_records)

    @app.route("/wapi/v2.12/record:cname", methods=["POST"])
    def create_cname_record():
        """POST /wapi/v2.12/record:cname - Create CNAME record."""
        data = request.get_json()
        if not data.get("name") or not data.get("canonical"):
            return jsonify({"error": "name and canonical required"}), 400

        record = {
            "name": data["name"],
            "canonical": data["canonical"],
            "record_type": "CNAME",
            "comment": data.get("comment"),
            "ttl": data.get("ttl"),
        }
        result = data_store.add_dns_record(record)
        return jsonify(result), 201

    @app.route("/wapi/v2.12/record:ptr", methods=["GET"])
    def get_ptr_records():
        """GET /wapi/v2.12/record:ptr - List PTR records."""
        filters = {}
        if request.args.get("ptrdname"):
            filters["ptrdname"] = request.args.get("ptrdname")
        if request.args.get("ipv4addr"):
            filters["ipv4addr"] = request.args.get("ipv4addr")

        records = data_store.get_dns_records(filters)
        # Filter to only PTR records
        ptr_records = [
            r for r in records if r.get("record_type", "").upper() == "PTR"
        ]
        return jsonify(ptr_records)

    @app.route("/wapi/v2.12/record:ptr", methods=["POST"])
    def create_ptr_record():
        """POST /wapi/v2.12/record:ptr - Create PTR record."""
        data = request.get_json()
        if not data.get("ptrdname") or not data.get("ipv4addr"):
            return jsonify({"error": "ptrdname and ipv4addr required"}), 400

        record = {
            "ptrdname": data["ptrdname"],
            "ipv4addr": data["ipv4addr"],
            "record_type": "PTR",
            "comment": data.get("comment"),
            "ttl": data.get("ttl"),
        }
        result = data_store.add_dns_record(record)
        return jsonify(result), 201

    @app.route("/wapi/v2.12/<path:ref>", methods=["DELETE"])
    def delete_record(ref: str):
        """DELETE /wapi/v2.12/<ref> - Delete record by reference."""
        if data_store.delete_dns_record(ref):
            return "", 204
        return jsonify({"error": "Record not found"}), 404
