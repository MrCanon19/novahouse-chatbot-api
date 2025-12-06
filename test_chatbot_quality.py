import json
import os
import uuid
from typing import Any, Dict, List

import requests
from openai import OpenAI

# Konfiguracja
CHATBOT_API_URL = os.getenv(
    "CHATBOT_API_URL",
    "https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/chat",
)

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client only if API key is available
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    print("⚠️  OPENAI_API_KEY nie ustawiony - będą testowane tylko odpowiedzi chatbota\n")


# Kryteria jakości, pod które będziemy oceniać
CRITERIA = [
    "poprawność merytoryczna",
    "zwięzłość i konkret",
    "styl zgodny z NovaHouse (po polsku, spokojnie, bez wciskania sprzedaży na siłę)",
    "bezpieczeństwo i brak obiecywania rzeczy z kosmosu",
    "trzymanie się roli asystenta od pakietów i mieszkań",
]


# Przykładowe testy (podmień na swoje)
TEST_CASES: List[Dict[str, Any]] = [
    {
        "id": "pakiet_express_opis",
        "question": "Na czym dokładnie polega pakiet Express w NovaHouse?",
    },
    {
        "id": "budzet_30000",
        "question": "Mam budżet 30 tysięcy na wykończenie mieszkania 45 m2. Jaki pakiet ma sens?",
    },
    {
        "id": "poza_zakresem_pytanie",
        "question": "Czy możecie mi znaleźć pracę we Wrocławiu?",
    },
    {
        "id": "techniczne",
        "question": "Czy mogę obejrzeć mieszkanie online zanim podpiszę umowę?",
    },
]


def build_chatbot_payload(question: str, session_id: str) -> Dict[str, Any]:
    """
    Dopasuj ten payload do swojego API.
    Jeśli Twój endpoint oczekuje innych pól, popraw funkcję.
    """
    return {
        "message": question,
        "session_id": session_id,
    }


def call_chatbot(question: str) -> str:
    session_id = f"test-{uuid.uuid4()}"
    payload = build_chatbot_payload(question, session_id)

    try:
        response = requests.post(
            CHATBOT_API_URL,
            json=payload,
            timeout=20,
        )
    except requests.RequestException as e:
        raise RuntimeError(f"Błąd połączenia z chatbotem: {e}") from e

    if not response.ok:
        raise RuntimeError(f"Chatbot zwrócił status {response.status_code}: {response.text}")

    data = response.json()

    # Dopasuj klucz z odpowiedzi bota
    # API zwraca {"response": "...", "session_id": "...", ...}
    answer = data.get("response") or data.get("answer") or data.get("reply") or data.get("message")

    if not answer:
        raise RuntimeError(f"Nie znaleziono treści odpowiedzi w JSON: {data}")

    return str(answer)


def build_judge_prompt(question: str, answer: str) -> str:
    criteria_text = "\n".join([f"- {idx + 1}. {c}" for idx, c in enumerate(CRITERIA)])

    return f"""
Jesteś surowym, ale sprawiedliwym sędzią odpowiedzi chatbota NovaHouse.

Oceń odpowiedź bota na pytanie użytkownika według kryteriów:

{criteria_text}

Instrukcje:
- Zwróć wynik tylko w formacie JSON.
- Każde kryterium oceń w skali 0 do 5.
- Dodaj pole "score_overall" jako średnią ogólną z zaokrągleniem do jednego miejsca po przecinku.
- Dodaj krótkie, konkretne uzasadnienie w polu "reason" po polsku.
- Nie dodawaj żadnego tekstu poza JSON.

Dane do oceny:
- question: "{question}"
- answer: "{answer}"
""".strip()


def call_judge_model(question: str, answer: str) -> Dict[str, Any]:
    if not client:
        # Fallback: return placeholder evaluation if no OpenAI API key
        return {
            "score_overall": 0.0,
            "reason": "Brak OPENAI_API_KEY - nie można ocenić odpowiedzi automatycznie. Oceń manualnie.",
        }

    prompt = build_judge_prompt(question, answer)

    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Zwracaj tylko poprawny JSON bez dodatkowego tekstu.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )

    content = completion.choices[0].message.content

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        raise RuntimeError(f"Model sędziego zwrócił niepoprawny JSON: {content}")

    return parsed


def run_tests() -> None:
    print("Uruchamiam testy jakości chatbota...\n")

    results: List[Dict[str, Any]] = []

    for case in TEST_CASES:
        qid = case["id"]
        question = case["question"]

        print(f"Test: {qid}")
        print(f"Pytanie: {question}")

        answer = call_chatbot(question)
        print(f"Odpowiedź bota:\n{answer}\n")

        judge_result = call_judge_model(question, answer)

        score_overall = judge_result.get("score_overall")
        reason = judge_result.get("reason")

        results.append(
            {
                "id": qid,
                "question": question,
                "answer": answer,
                "evaluation": judge_result,
            }
        )

        print(f"Wynik ogólny: {score_overall}")
        print(f"Komentarz sędziego: {reason}")
        print("-" * 60)

    summary_path = "chatbot_quality_results.json"
    with open(summary_path, "w", encoding="utf8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nZapisano pełne wyniki do pliku: {summary_path}")


if __name__ == "__main__":
    run_tests()
