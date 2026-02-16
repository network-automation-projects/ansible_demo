"""
Minimal Flask REST API skeleton.
Copy and add routes. Use for interview or new microservice.
Optional CORS: pip install flask-cors then add: from flask_cors import CORS; CORS(app)
"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health() -> tuple:
    """GET example: return JSON and 200."""
    return jsonify({"status": "ok"}), 200


@app.route("/items", methods=["GET"])
def list_items() -> tuple:
    """GET example: return a list (replace with real data)."""
    items = [{"id": 1, "name": "example"}]
    return jsonify({"items": items}), 200


@app.route("/items", methods=["POST"])
def create_item() -> tuple:
    """POST example: read JSON body and return created resource."""
    data = request.get_json(silent=True) or {}
    name = data.get("name", "unnamed")
    # Replace with real create logic and id generation
    return jsonify({"id": 1, "name": name}), 201


@app.errorhandler(404)
def not_found(e: Exception) -> tuple:
    """Return JSON for 404."""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(e: Exception) -> tuple:
    """Return JSON for 500."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
