"""Lokalny klient terminalowy dla NovaHouse chatbota.

Użycie (w drugim terminalu po odpaleniu backendu):
    python chat_client.py

Komendy:
    /file <ścieżka>  – wyślij plik do analizy
    /apply <ścieżka> – nadpisz plik kodem z ostatniej odpowiedzi (tworzy .bak)
    /exit            – zakończ
"""

import json
import shutil
from pathlib import Path
import requests

API_URL = "http://127.0.0.1:5050/chat"
DEFAULT_CONVERSATION_ID = "local-dev-session"


def send_message(message: str, conversation_id: str | None = None) -> dict:
    payload: dict[str, object] = {
        "message": message,
    }
    if conversation_id:
        payload["conversation_id"] = conversation_id

    response = requests.post(API_URL, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()


def extract_reply(data: dict) -> str:
    """Spróbuj wydobyć odpowiedź tekstową z kilku typowych kluczy."""

    if isinstance(data, dict):
        resp = data.get("response")
        if isinstance(resp, str):
            return resp

    # Dopasowane do typowych struktur odpowiedzi
    for key in ["assistant_message", "reply", "message", "content"]:
        value = data.get(key) if isinstance(data, dict) else None
        if isinstance(value, str):
            return value

    return json.dumps(data, ensure_ascii=False, indent=2)


def read_file(path_str: str) -> str:
    path = Path(path_str).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Plik nie istnieje: {path}")
    return path.read_text(encoding="utf-8")


def write_file_from_reply(path_str: str, reply: str) -> None:
    """
    Szuka pierwszego fenced code blocka w odpowiedzi:
    ```python
    ...kod...
    ```
    i zapisuje go do pliku.
    """
    if not reply:
        raise ValueError("Brak odpowiedzi bota do zapisania")

    start = reply.find("```")
    if start == -1:
        raise ValueError("Nie znaleziono bloku kodu ``` w odpowiedzi bota")

    # Znajdź koniec pierwszego bloku
    end = reply.find("```", start + 3)
    if end == -1:
        raise ValueError("Znaleziono otwarcie ``` ale brak zamknięcia")

    code_block = reply[start + 3:end]

    # Usuń ewentualny znacznik języka z pierwszej linii
    lines = code_block.splitlines()
    if lines and lines[0].strip().startswith(("python", "py")):
        lines = lines[1:]
    code = "\n".join(lines).strip("\n") + "\n"

    path = Path(path_str).expanduser().resolve()
    if path.exists():
        backup_path = path.with_suffix(path.suffix + ".bak")
        shutil.copy2(path, backup_path)

    path.write_text(code, encoding="utf-8")


def print_help() -> None:
    print(
        "Dostępne komendy:\n"
        "  /file ŚCIEŻKA   - wyślij zawartość pliku do analizy\n"
        "  /apply ŚCIEŻKA  - zapisz kod z ostatniej odpowiedzi bota do pliku\n"
        "  /exit           - zakończ\n"
    )


def main() -> None:
    print("Lokalny asystent programistyczny")
    print_help()
    print("Napisz /exit aby zakończyć.\n")

    conversation_id = DEFAULT_CONVERSATION_ID
    last_reply: str | None = None

    while True:
        try:
            user_input = input("Ty: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nKończę.")
            break

        if not user_input:
            continue

        # Komenda wyjścia
        if user_input.lower() in {"/exit", "quit", "q"}:
            print("Kończę.")
            break

        # Pomoc
        if user_input.lower() in {"/help", "help"}:
            print_help()
            continue

        # Wysyłanie pliku do analizy
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
                f"Here is the file `{path_str}`. "
                f"Please review it and suggest improvements. "
                f"Return the full improved file in a single code block.\n\n"
                f"```python\n{content}\n```")
            try:
                data = send_message(message, conversation_id=conversation_id)
                reply = extract_reply(data)
                last_reply = reply
                print(f"\nBot:\n{reply}\n")
            except Exception as e:
                print(f"[Błąd requestu] {e}\n")
            continue

        # Zastosowanie zmian z ostatniej odpowiedzi bota
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
                print(f"Zapisano zmiany do pliku: {path_str}\n")
            except Exception as e:
                print(f"[Błąd zapisu pliku] {e}\n")
            continue

        # Zwykła wiadomość tekstowa
        try:
            data = send_message(user_input, conversation_id=conversation_id)
            reply = extract_reply(data)
            last_reply = reply
            print(f"Bot:\n{reply}\n")
        except Exception as e:
            print(f"[Błąd requestu] {e}\n")


if __name__ == "__main__":
    main()
