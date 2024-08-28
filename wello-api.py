from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Store the last ping time for each host
host_status = {}

# Secure API key
SECURE_API_KEY = "your-secure-api-key"

@app.route("/ping", methods=["POST"])
def ping():
    # Verify the API key
    auth_header = request.headers.get('Authorization')
    if auth_header != f'Bearer {SECURE_API_KEY}':
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    hostname = data.get('hostname')

    if not hostname:
        return jsonify({"error": "Hostname is required"}), 400

    # Update the last ping time for the host
    host_status[hostname] = time.time()
    return jsonify({"message": "Ping received"}), 200

@app.route("/ping", methods=["GET", "PUT", "DELETE", "PATCH"])
def reject_non_post_requests():
    return jsonify({"error": "Method not allowed"}), 405

# To view the status of hosts (for debugging purposes)
@app.route("/status", methods=["GET"])
def status():
    return jsonify(host_status), 200

if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=5000, debug=True)
