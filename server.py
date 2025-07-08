from flask import Flask, request, jsonify
import requests

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
     "Content-Type": "application/json",
}

@app.route("/waifu",  methods=["POST"])
def waifu():
    data = request.get_json()
    user_message = data.get("message","")
  
    if not user_message:
      return jsonify({"error":
"Message vide"}), 400

     # Message envoyé a l'IA
    payload = {
         "model": "mistral", # ou "gpt-3.5-turbo", "llama-3" etc.
         "messages": [
             {"role": "system",
"content": "Tu es une waifu mignonne et gentille qui répond avec un style animé."},

             {"role": "user", "content":
user_message},
        ]
    }

    try:
        response = requests.post(OPENROUTER_URL,
headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        ai_reply = result["choices"][0] ["message"]["content"]

        return jsonify({"response": ai_reply})

    except Exception as e:
        return jsonify({"error":
str(e)}), 500

if __name__ =="__main__":
  app.run()
