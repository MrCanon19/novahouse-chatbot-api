import json
import requests

API_URL = "http://127.0.0.1:5050/chat"


def send_message(message: str, conversation_id: str | None = None) -> str:
    payload = {
        "message": message,
    }
    if conversation_id:
        payload["conversation_id"] = conversation_id

    response = requests.post(API_URL, json=payload, timeout=60)
    response.raise_for_status()

    data = response.json()

    for key in ["assistant_message", "reply", "message", "content"]:
        if isinstance(data, dict) and key in data and isinstance(data[key], str):
            return data[key]

    return json.dumps(data, ensure_ascii=False, indent=2)


def main() -> None:
    print("Lokalny chatbot NovaHouse")
    print("Napisz /exit aby zakończyć.\n")

    conversation_id = "local-dev-session"

    while True:
        try:
            user_input = input("Ty: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nKończę.")
            break

        if not user_input:
            continue
        if user_input.lower() in {"/exit", "quit", "q"}:
            print("Kończę.")
            break

        try:
            reply = send_message(user_input, conversation_id=conversation_id)
        except Exception as exc:  # noqa: BLE001
            print(f"[Błąd requestu] {exc}")
            continue

        print(f"Bot: {reply}\n")


if __name__ == "__main__":
    main()
