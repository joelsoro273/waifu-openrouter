
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
 
app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return "Waifu server est en ligne"

@app.route("/waifu", methods=["POST"])
def waifu_reply():
    try:
        data = request.get_json()
        message = data.get("message", "")
        if not message:
            return jsonify({"error": "Message manquant"}), 400
        if not OPENROUTER_API_KEY:
            return jsonify({"error": "Clé API OpenRouter manquante"}), 500

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://waifu-chat.app",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": message}
            ]
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return jsonify({
                "error": f"{response.status_code} Client Error: {response.reason} for url: {url}"
            }), 500

        reply = response.json() ["choices"][0]["message"]["content"]

        return jsonify({
            "reply": reply,
            "video_url": f"https://fake.video.generator/video?text={reply}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True, port=5000)

