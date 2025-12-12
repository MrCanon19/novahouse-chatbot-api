# 🔍 Wyjaśnienie Błędów 502

## Błędy które widzisz:

### 1. `content.js:1 Uncaught (in promise) The message port closed before a response was received`

**Co to oznacza:**
- To **NIE jest błąd Twojej aplikacji**!
- To błąd z **rozszerzenia przeglądarki** (np. AdBlock, LastPass, inne rozszerzenia)
- Rozszerzenie próbowało komunikować się z content script, ale połączenie zostało zamknięte

**Czy to problem?**
- ❌ **NIE** - możesz to zignorować
- To nie wpływa na działanie aplikacji
- Możesz wyłączyć rozszerzenia przeglądarki, żeby nie widzieć tego błędu

**Jak naprawić (opcjonalnie):**
- Wyłącz rozszerzenia przeglądarki
- Lub zignoruj ten błąd - nie wpływa na aplikację

---

### 2. `/favicon.ico:1 Failed to load resource: the server responded with a status of 502`

**Co to oznacza:**
- **502 Bad Gateway** = serwer nie może uruchomić aplikacji
- Aplikacja Flask nie startuje poprawnie
- Gunicorn (serwer WSGI) nie może załadować aplikacji

**Przyczyna:**
- Błąd składni w kodzie (IndentationError, SyntaxError)
- Błąd importu modułów
- Brakujące zależności
- Błąd podczas inicjalizacji aplikacji

**Jak naprawić:**
1. Sprawdź logi aplikacji:
   ```bash
   python3 scripts/monitor_logs.py --errors --limit 10
   ```

2. Sprawdź składnię lokalnie:
   ```bash
   python3 -m py_compile src/routes/chatbot.py
   ```

3. Sprawdź import aplikacji:
   ```bash
   python3 -c "from src.main import app; print('OK')"
   ```

4. Jeśli wszystko OK lokalnie, wdróż ponownie:
   ```bash
   ./scripts/deploy_production.sh
   ```

---

### 3. `chatbot.html:1 Failed to load resource: the server responded with a status of 502`

**Co to oznacza:**
- To samo co powyżej - aplikacja nie działa
- Przeglądarka próbuje załadować `chatbot.html`, ale serwer zwraca 502

**Przyczyna:**
- Ta sama co powyżej - aplikacja nie startuje

**Jak naprawić:**
- Napraw błąd składni/importu
- Wdróż ponownie aplikację

---

## 🔧 Diagnostyka Błędu 502

### Krok 1: Sprawdź logi błędów

```bash
python3 scripts/monitor_logs.py --errors --limit 20
```

Szukaj:
- `IndentationError`
- `SyntaxError`
- `ModuleNotFoundError`
- `ImportError`
- `Worker failed to boot`

### Krok 2: Sprawdź składnię lokalnie

```bash
# Sprawdź składnię wszystkich plików
python3 -m py_compile src/routes/chatbot.py
python3 -m py_compile src/main.py
```

### Krok 3: Sprawdź import aplikacji

```bash
python3 -c "from src.main import app; print('✅ OK')"
```

### Krok 4: Jeśli wszystko OK, wdróż ponownie

```bash
./scripts/deploy_production.sh
```

---

## ✅ Najczęstsze Przyczyny 502

1. **Błąd składni (IndentationError, SyntaxError)**
   - Napraw: Sprawdź wcięcia i składnię
   - Sprawdź: `python3 -m py_compile plik.py`

2. **Błąd importu**
   - Napraw: Sprawdź czy wszystkie moduły są dostępne
   - Sprawdź: `python3 -c "from src.main import app"`

3. **Brakujące zależności**
   - Napraw: Sprawdź `requirements.txt`
   - Sprawdź: Czy wszystkie pakiety są zainstalowane

4. **Błąd podczas inicjalizacji**
   - Napraw: Sprawdź logi aplikacji
   - Sprawdź: Czy wszystkie zmienne środowiskowe są ustawione

---

## 📊 Status Naprawy

**Ostatnia naprawa:** IndentationError w `chatbot.py` linia 254
- ✅ Naprawiono brakujące wcięcie
- ✅ Aplikacja powinna teraz działać

**Sprawdź status:**
```bash
curl https://glass-core-467907-e9.ey.r.appspot.com/api/health
```

Powinno zwrócić: `200 OK` (nie `502`)

