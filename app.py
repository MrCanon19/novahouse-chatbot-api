import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from groq import Groq

load_dotenv()

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
CHATBOT_MODE = os.getenv("CHATBOT_MODE", "stub")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "Jesteś asystentem NovaHouse.")
PORT = int(os.getenv("PORT", 5050))

# ─────────────────────────────────────────────
# FLASK SETUP
# ─────────────────────────────────────────────
app = Flask(__name__)
CORS(app)


# ─────────────────────────────────────────────
# HEALTHCHECK
# ─────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "mode": CHATBOT_MODE})


# ─────────────────────────────────────────────
# CHAT ENDPOINT
# ─────────────────────────────────────────────
@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        data = request.get_json()
        if not data or "messages" not in data:
            return jsonify({"error": "Brak wiadomości"}), 400

        # Wstrzykuj system prompt
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in data["messages"]:
            messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})

        # ─────────────────────────────────────────────
        # STUB MODE (bez kosztów)
        # ─────────────────────────────────────────────
        if CHATBOT_MODE == "stub":
            return jsonify(
                {"mode": "stub", "reply": f"Stub: Odebrałem wiadomość: {messages[-1]['content']}"}
            )

        # ─────────────────────────────────────────────
        # GROQ MODE
        # ─────────────────────────────────────────────
        if CHATBOT_MODE == "groq":

            if not GROQ_API_KEY:
                return jsonify({"error": "Brak GROQ_API_KEY"}), 500

            client = Groq(api_key=GROQ_API_KEY)

            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
            )

            # POPRAWKA: Groq zwraca OBIEKT, nie dict
            content = response.choices[0].message.content

            return jsonify({"reply": content})

        return jsonify({"error": "Nieznany tryb bota"}), 500

    except Exception as e:
        return jsonify({"error": "Błąd serwera", "details": str(e)}), 500


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print(f"NovaHouse Chatbot backend running on port {PORT} in mode: {CHATBOT_MODE}")
    app.run(host="0.0.0.0", port=PORT, debug=True)
