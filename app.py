from flask import Flask, request, jsonify
import requests
import os
import json

app = Flask(__name__)

API_URL = "https://prowessed-meta-semioratorically.ngrok-free.dev/search?num={}"
OWNER = "@ravenxankit"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "ngrok-skip-browser-warning": "true"
}

@app.route("/")
def home():
    return jsonify({
        "status": "running ✅",
        "usage": "/get?num=9876543210",
        "owner": OWNER
    })

@app.route("/get")
def get_info():
    num = request.args.get("num", "").strip()

    if not num.isdigit() or not (10 <= len(num) <= 12):
        return jsonify({
            "error": "Invalid number format",
            "owner": OWNER
        }), 400

    try:
        r = requests.get(
            API_URL.format(num),
            headers=HEADERS,
            timeout=10
        )

        # ngrok html page check
        if r.text.lstrip().startswith("<!DOCTYPE html"):
            return jsonify({
                "error": "ngrok security page detected",
                "owner": OWNER
            }), 502

        if r.status_code != 200:
            return jsonify({
                "error": "Upstream API failed",
                "status_code": r.status_code,
                "owner": OWNER
            }), 502

        raw = r.text.strip()

        # 🔥 FIX HERE
        try:
            parsed_data = json.loads(raw)
        except json.JSONDecodeError:
            parsed_data = raw

        return jsonify({
            "number": num,
            "data": parsed_data,
            "owner": OWNER,
            "source": "ngrok-api"
        })

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Request timeout",
            "owner": OWNER
        }), 504

    except Exception as e:
        return jsonify({
            "error": "Server error",
            "detail": str(e),
            "owner": OWNER
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
