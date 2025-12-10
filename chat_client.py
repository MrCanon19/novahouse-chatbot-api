import json
import shutil
from pathlib import Path

import requests

API_URL = "http://127.0.0.1:5050/api/chatbot/chat"
DEFAULT_CONVERSATION_ID = "local-dev-session"


def send_message(message, conversation_id=None):
    payload = {"message": message}
    if conversation_id:
        payload["conversation_id"] = conversation_id

    resp = requests.post(API_URL, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()


def extract_reply(data):
    for key in ["assistant_message", "reply", "message", "content"]:
        value = data.get(key)
        if isinstance(value, str):
            return value
    return json.dumps(data, ensure_ascii=False, indent=2)


def read_file(path_str):
    path = Path(path_str).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Plik nie istnieje: {path}")
    return path.read_text(encoding="utf-8")


def backup_file(path):
    src = Path(path).expanduser().resolve()
    if src.is_file():
        bak = src.with_suffix(src.suffix + ".bak")
        shutil.copy2(src, bak)


def write_file_from_reply(path_str, reply):
    if not reply:
        raise ValueError("Brak odpowiedzi bota do zapisania")

    start = reply.find("```")
    if start == -1:
        raise ValueError("Nie znaleziono bloku kodu ``` w odpowiedzi bota")

    end = reply.find("```", start + 3)
    if end == -1:
        raise ValueError("Znaleziono otwarcie ``` ale brak zamknięcia")

    code_block = reply[start + 3 : end]
    lines = code_block.splitlines()
    if lines and lines[0].strip().startswith(("python", "py")):
        lines = lines[1:]
    code = "\n".join(lines).strip("\n") + "\n"

    path = Path(path_str).expanduser().resolve()
    backup_file(path)
    path.write_text(code, encoding="utf-8")


def print_help():
    print(
        "Dostępne komendy:\n"
        "  /file ŚCIEŻKA   - wyślij zawartość pliku do analizy i refaktoru\n"
        "  /apply ŚCIEŻKA  - zapisz kod z ostatniej odpowiedzi bota do pliku (.bak jako backup)\n"
        "  /help           - pokazuje tę pomoc\n"
        "  /exit           - zakończ\n"
    )


def main():
    print("Lokalny asystent programistyczny NovaHouse")
    print("Użycie: /file, /apply, /help, /exit\n")
    print_help()
    print()

    conversation_id = DEFAULT_CONVERSATION_ID
    last_reply = None

    while True:
        try:
            user_input = input("Ty: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nKończę.")
            break

        if not user_input:
            continue

        cmd = user_input.lower()

        if cmd in {"/exit", "quit", "q"}:
            print("Kończę.")
            break

        if cmd in {"/help", "help"}:
            print_help()
            continue

        if user_input.startswith("/file "):
            path_str = user_input[len("/file ") :].strip()
            if not path_str:
                print("Podaj ścieżkę do pliku, np. /file src/services/llm/engine.py\n")
                continue
            try:
                content = read_file(path_str)
            except Exception as e:
                print(f"[Błąd czytania pliku] {e}\n")
                continue

            message = (
                f"Here is the file `{path_str}`.\n"
                f"Review it as a senior engineer. Suggest improvements and return the full improved file in one code block.\n\n"
                f"```python\n{content}\n```"
            )
            try:
                data = send_message(message, conversation_id=conversation_id)
                reply = extract_reply(data)
                last_reply = reply
                print(f"\nBot:\n{reply}\n")
            except Exception as e:
                print(f"[Błąd requestu] {e}\n")
            continue

        if user_input.startswith("/apply "):
            path_str = user_input[len("/apply ") :].strip()
            if not path_str:
                print("Podaj ścieżkę do pliku, np. /apply src/services/llm/engine.py\n")
                continue
            if not last_reply:
                print("Brak ostatniej odpowiedzi bota z kodem do zapisania.\n")
                continue
            try:
                write_file_from_reply(path_str, last_reply)
                print(f"Zapisano zmiany do pliku (backup .bak): {path_str}\n")
            except Exception as e:
                print(f"[Błąd zapisu pliku] {e}\n")
            continue

        try:
            data = send_message(user_input, conversation_id=conversation_id)
            reply = extract_reply(data)
            last_reply = reply
            print(f"Bot:\n{reply}\n")
        except Exception as e:
            print(f"[Błąd requestu] {e}\n")


if __name__ == "__main__":
    main()
