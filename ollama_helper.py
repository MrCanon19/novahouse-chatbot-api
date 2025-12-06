import sys
import textwrap

import requests

API_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:7b"


def ask_ollama(prompt: str) -> str:
    print(f"[DEBUG] Wysyłam zapytanie do Ollama z modelem {MODEL}...")
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    try:
        resp = requests.post(API_URL, json=payload, timeout=120)
        print(f"[DEBUG] Kod odpowiedzi HTTP: {resp.status_code}")
        print(f"[DEBUG] Surowa odpowiedź: {resp.text[:400]}...")
        resp.raise_for_status()
    except Exception as e:
        print("[ERROR] Problem z połączeniem do Ollama lub odpowiedzią API")
        print(e)
        raise

    data = resp.json()
    # Spróbujmy kilka wariantów struktury
    if "message" in data and "content" in data["message"]:
        return data["message"]["content"]
    if "choices" in data and data["choices"]:
        msg = data["choices"][0].get("message", {})
        return msg.get("content", str(data))
    return str(data)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = sys.stdin.read()

    print(f"[INFO] Prompt: {prompt!r}")

    answer = ask_ollama(prompt)
    print("\n" + "-" * 40 + "\n")
    print(textwrap.fill(answer, width=100))
    print("\n" + "-" * 40 + "\n")
