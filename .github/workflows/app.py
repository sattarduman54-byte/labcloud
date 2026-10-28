
from flask import Flask, jsonify, request

app = Flask(__name__)
requests_data = []
next_id = 1


@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "application": "LabCloud",
        "environment": "development",
        "status": "running"
    })


@app.route("/requests", methods=["GET", "POST"])
def requests_endpoint():
    global next_id

    if request.method == "GET":
        return jsonify(requests_data)

    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    item = {
        "id": next_id,
        "title": title.strip(),
        "description": data.get("description", ""),
        "category": data.get("category", "general")
    }
    requests_data.append(item)
    next_id += 1

    return jsonify(item), 201


@app.route("/requests/<int:request_id>", methods=["GET"])
def get_request(request_id):
    for item in requests_data:
        if item["id"] == request_id:
            return jsonify(item)
    return jsonify({"error": "Request not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
