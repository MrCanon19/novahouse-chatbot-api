# Testy wydajnościowe NovaHouse Chatbot

Do testów wydajnościowych rekomendowane narzędzia:
- Locust (Python): testy obciążeniowe dla API
- k6 (JavaScript): testy dla endpointów HTTP

## Przykład testu Locust
```python
from locust import HttpUser, task, between

class ChatbotUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def send_message(self):
        self.client.post("/api/chat", json={"message": "Cześć!"})
```
Uruchom: `locust -f locustfile.py --host=https://twoja-domena`

## Przykład testu k6
```js
import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
  http.post('https://twoja-domena/api/chat', JSON.stringify({ message: 'Cześć!' }), { headers: { 'Content-Type': 'application/json' } });
  sleep(1);
}
```
Uruchom: `k6 run k6_test.js`

## Zalecenia
- Testuj kluczowe endpointy: /api/chat, /booking/create, /api/widgets/metrics/summary
- Ustaw limity i alerty na czas odpowiedzi, liczbę błędów, obciążenie CPU/RAM
- Wyniki testów zapisuj w logach i monitoruj regularnie

Szczegóły i przykłady w dokumentacji Locust/k6.
