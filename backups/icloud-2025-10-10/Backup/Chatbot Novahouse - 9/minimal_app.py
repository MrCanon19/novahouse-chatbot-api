'''
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return "OK"

@app.route("/api/chatbot/chat", methods=["POST"])
def chat():
    return jsonify({"response": "Cześć! Działam poprawnie."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
'''
