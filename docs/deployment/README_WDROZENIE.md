# NovaHouse Chatbot - Szybki Start Wdrożenia na GCP

## 🚀 Szybkie Wdrożenie (5 minut)

### Wymagania
- Konto Google Cloud Platform z włączoną płatnością
- Zainstalowany Google Cloud SDK (`gcloud`)

### Kroki Wdrożenia

1. **Zaloguj się i ustaw projekt:**
```bash
gcloud auth login
gcloud config set project TWOJ-PROJEKT-ID
```

2. **Włącz App Engine:**
```bash
gcloud app create --region=europe-west3
```

3. **Wdróż aplikację:**
```bash
gcloud app deploy app.yaml --quiet
```

4. **Sprawdź URL aplikacji:**
```bash
gcloud app browse
```

### Testowanie
- **Health Check:** `https://TWOJ-PROJEKT-ID.appspot.com/api/health`
- **Chatbot:** `https://TWOJ-PROJEKT-ID.appspot.com/static/chatbot.html`

### Dokumentacja Szczegółowa
Zobacz plik `INSTRUKCJA_WDROZENIA_GCP.md` dla pełnej instrukcji.

### Wsparcie
W przypadku problemów skontaktuj się z zespołem deweloperskim.

---
*Wygenerowano przez Manus AI - 11 sierpnia 2025*

