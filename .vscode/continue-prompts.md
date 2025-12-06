# 🤖 Continue.dev - Przykładowe Prompty

## Gotowe do użycia prompty dla tego projektu

### 🔍 Analiza kodu

```
@codebase Wyjaśnij mi jak działa system chatbota - od odebrania wiadomości do odpowiedzi
```

```
@code Znajdź wszystkie miejsca gdzie używamy OpenAI API i pokaż mi konfigurację
```

```
@folder src/routes Pokaż mi wszystkie endpointy API i opisz co robią
```

### 🛠️ Dodawanie funkcjonalności

```
Dodaj nowy endpoint POST /api/leads/export który eksportuje leady do CSV.
Użyj istniejącego stylu z src/routes/backup.py jako wzór.
```

```
Dodaj funkcję walidacji numeru telefonu do src/models/chatbot.py która sprawdza czy numer jest w formacie polskim (+48)
```

```
Stwórz nowy test dla endpointu /api/chat w tests/test_chatbot.py który sprawdza rate limiting
```

### 🐛 Debugowanie

```
@problems Wyjaśnij mi te błędy i zaproponuj poprawki
```

```
@terminal Przeanalizuj ten stack trace i powiedz co poszło nie tak
```

```
@diff Przejrzyj moje zmiany i sprawdź czy nie wprowadziłem bugów
```

### 📝 Refaktoryzacja

```
@code Zrefaktoruj tę funkcję żeby była bardziej czytelna i dodaj type hints
```

```
Ta funkcja jest za długa - podziel ją na mniejsze funkcje zgodnie z zasadą single responsibility
```

```
Znajdź duplikację kodu w src/routes/ i zaproponuj wspólne funkcje pomocnicze
```

### 🧪 Testy

```
Napisz kompletny test jednostkowy dla src/services/rate_limiter.py
Pokryj wszystkie przypadki brzegowe.
```

```
Dodaj testy integracyjne dla src/routes/booking.py - sprawdź happy path i error cases
```

```
Wygeneruj mock dla OpenAI API w testach, żeby nie wywoływać prawdziwego API
```

### 📚 Dokumentacja

```
Dodaj docstringi w stylu Google dla wszystkich funkcji w src/routes/chatbot.py
```

```
Wygeneruj README.md dla folderu src/services/ z opisem każdego serwisu
```

```
Stwórz przykłady użycia API dla endpointu /api/chat z różnymi parametrami
```

### 🔧 Konfiguracja

```
Przeanalizuj app.yaml.example i wyjaśnij każde ustawienie
```

```
@docs Znajdź w dokumentacji jak skonfigurować Redis i pokaż mi przykład
```

```
Porównaj config/docker-compose.yml z dokumentacją i sprawdź czy wszystko jest aktualne
```

### 🚀 Deployment

```
Sprawdź plik .github/workflows/ci-cd.yml i zaproponuj ulepszenia
```

```
Przeanalizuj logi z last deploy i powiedz czy są jakieś warningi do naprawienia
```

```
Zrób checklist deployment readiness - co trzeba sprawdzić przed wdrożeniem?
```

## 💡 Wskazówki

### Używaj context providers:

- `@codebase` - przeszukuje całe repo
- `@code` - aktualny otwarty plik
- `@folder` - konkretny folder
- `@docs` - dokumentacja projektu
- `@terminal` - output z terminala
- `@problems` - błędy z VS Code
- `@diff` - niezatwierdzone zmiany

### Przykład kompleksowego prompta:

```
@codebase Chcę dodać system notyfikacji email dla nowych leadów.

1. Znajdź gdzie są zapisywane leady (src/routes/leads.py)
2. Sprawdź czy mamy już jakąś integrację email (powinno być w src/integrations/)
3. Dodaj funkcję send_lead_notification() w nowym pliku src/services/email_notifications.py
4. Użyj SMTP z konfiguracji z .env
5. Dodaj wywołanie tej funkcji po zapisaniu leada
6. Dodaj testy w tests/test_email_notifications.py
7. Dodaj dokumentację do docs/

Pokaż mi step-by-step implementację z kodem.
```

## 🎯 Najlepsze praktyki dla tego projektu

1. **Zawsze używaj Blueprint pattern** dla nowych routes
2. **Migrations przez HTTP endpoints** - nie Alembic auto-migration
3. **Rate limiting** - dodaj decorator `@rate_limit()` do publicznych endpointów
4. **Error handling** - używaj specyficznych wyjątków, nie generycznych
5. **Tests** - pytest, sprawdź `tests/conftest.py` dla fixtures
6. **Code style** - Black (line length 100), uruchom `make format` przed commitem

## 🔗 Przydatne komendy

```bash
# Formatowanie
make format

# Testy
make test

# Linting
make lint

# Docker
make docker

# Deployment smoke tests
python tests/smoke_tests.py https://your-app-url.com
```
