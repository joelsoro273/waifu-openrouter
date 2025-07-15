
from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv() 
app = Flask(__name__)

@app.route("/waifu",  methods=["POST"])
def waifu():
    try:
        data = request.get_json()
        message = data.get("message","")

        if not message:
            return jsonify({"error": "Aucun message reçu"}), 400

        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if not openrouter_api_key:
             return jsonify({"error": "Clé API OpenRouter manquante".}), 500

        headers = {
            "Authorization": f"Bearer {openrouter_api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "ministralai/ministral-7b-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()

        reply = response.json() ["choices"][0]["message"]["content"]
        
        "video_url": f"https://fake.video.generator/video?text={reply}"
        return jsonify({"video_url":video_url})
 
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if name == "main":
    app.run()

