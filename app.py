from flask import Flask, request, jsonify
import requests
import os

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

    # validation
    if not num.isdigit() or not (10 <= len(num) <= 12):
        return jsonify({
            "error": "Invalid number format",
            "example": "/get?num=9876543210",
            "owner": OWNER
        }), 400

    try:
        url = API_URL.format(num)
        r = requests.get(url, headers=HEADERS, timeout=10)

        # ngrok html protection check
        if r.text.lstrip().startswith("<!DOCTYPE html"):
            return jsonify({
                "error": "ngrok security page detected",
                "hint": "Free ngrok blocks API requests",
                "owner": OWNER
            }), 502

        if r.status_code != 200:
            return jsonify({
                "error": "Upstream API failed",
                "status_code": r.status_code,
                "owner": OWNER
            }), 502

        data = r.text.strip()
        if not data:
            return jsonify({
                "error": "No data found",
                "owner": OWNER
            }), 404

        return jsonify({
            "number": num,
            "data": data,
            "source": "ngrok-api",
            "owner": OWNER
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
