from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_URL = "https://xploide.site/Api.php?num={}"

@app.route("/")
def home():
    return jsonify({
        "message": "API is running!",
        "usage": "/get?num=987654321",
        "owner": "@Saksham24_11"
    })

@app.route("/get")
def get_info():
    num = request.args.get("num")

    if not num or not num.isdigit():
        return jsonify({
            "error": "Please provide a valid number ?num=1234567890",
            "owner": "@Saksham24_11"
        })

    try:
        url = API_URL.format(num)
        response = requests.get(url, timeout=10)

        if response.status_code == 200 and response.text.strip():
            return jsonify({
                "number": num,
                "result": response.text.strip(),
                "owner": "@Saksham24_11"
            })
        else:
            return jsonify({
                "error": "API did not return data",
                "owner": "@Saksham24_11"
            })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "owner": "@Saksham24_11"
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render/Heroku dynamic port
    app.run(host="0.0.0.0", port=port)