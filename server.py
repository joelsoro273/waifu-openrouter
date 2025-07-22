
import os
import json
import requests
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from gtts import gTTS
 
app = Flask(__name__)
CORS(app)

os.makedirs("static/audio", exist_ok=True)

with open("waifus.json", "r", encoding="utf-8") as f:
    WAIFUS = json.load(f)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return "Waifu server est en ligne"

@app.route("/waifus", methods=["GET"])
def get_waifus():
    return jsonify([{"name": w["name"], "avatar": w["avatar"]} for w in WAIFUS])

@app.route("/waifu", methods=["POST"])
def waifu_reply():
    try:
        data = request.get_json()
        message = data.get("message", "")
        waifu_name = data.get("waifu","")
        if not message:
            return jsonify({"error": "Message manquant"}), 400
        if not OPENROUTER_API_KEY:
            return jsonify({"error": "Clé API OpenRouter manquante"}), 500

        waifu = next((w for w in WAIFUS if w["name"].lower() == waifu_name.lower()), None)
        if not waifu:
            return jsonify({"error": "Waifu non trouvé"}), 404

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://waifu-chat.app",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": f"Tu es {waifu['name']}, une waifu d'anime japonaise qui répond avec douceur et style kawaii."},
                {"role": "user", "content": message}
            ]
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return jsonify({
                "error": f"{response.status_code} Client Error: {response.reason} for url: {url}"
            }), 500

        reply = response.json() ["choices"][0]["message"]["content"]

        tts = gTTS(text=reply, lang="fr")
        filename = f"{uuid.uuid4().hex}.mp3"
        audio_path = os.path.join("static/audio", filename)
        tts.save(audio_path)

        audio_url = request.host_url.rstrip("/") + "/" + audio_path

        return jsonify({
            "reply": reply,
            "avatar": waifu["avatar"],
            "video_url": f"https://fake.video.generator/video?text={reply}",
            "audio_url": audio_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True, port=5000)

