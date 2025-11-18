# Contributing to NovaHouse Chatbot

Dziękujemy za zainteresowanie! Każdy wkład jest mile widziany.

## 🚀 Quick Start

```bash
# 1. Fork & clone
git clone https://github.com/YOUR_USERNAME/novahouse-chatbot-api.git
cd novahouse-chatbot-api

# 2. Setup environment
cp .env.example .env
# Wypełnij .env swoimi danymi

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run tests
pytest tests/

# 5. Run locally
python src/main.py
```

## 📋 Development Process

### Branch Naming

- `feature/nazwa-funkcji` - nowe funkcje
- `fix/nazwa-buga` - poprawki błędów
- `docs/nazwa` - dokumentacja
- `refactor/nazwa` - refaktoryzacja

### Commit Messages

Format: `Type: Short description`

Types:

- `Feature:` - nowa funkcjonalność
- `Fix:` - naprawa błędu
- `Docs:` - dokumentacja
- `Refactor:` - refaktoryzacja
- `Test:` - testy
- `Chore:` - maintenance

Przykłady:

```
Feature: Dodano WhatsApp integration
Fix: Poprawiono KeyError w packages
Docs: Zaktualizowano README
```

### Pull Request Process

1. Utwórz branch z `main`
2. Wprowadź zmiany
3. Napisz/zaktualizuj testy
4. Uruchom testy: `pytest tests/`
5. Commit ze znaczącym message
6. Push do swojego forka
7. Otwórz Pull Request do `main`

### PR Checklist

- [ ] Kod działa lokalnie
- [ ] Testy przechodzą
- [ ] Brak konfliktów z `main`
- [ ] Dokumentacja zaktualizowana
- [ ] Code review requested
- [ ] CI/CD checks pass

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/test_chatbot.py::TestChatbotHealth
```

### Writing Tests

Umieść w `tests/`:

```python
def test_feature_name():
    """Test description"""
    # Arrange
    setup_data()

    # Act
    result = function_to_test()

    # Assert
    assert result == expected
```

## 📝 Code Style

### Python

- PEP 8 compliance
- Max line length: 120
- Use type hints where possible
- Docstrings for functions/classes

```python
def process_message(text: str, user_id: int) -> dict:
    """
    Process user message and generate response.

    Args:
        text: User's message
        user_id: User identifier

    Returns:
        dict with 'response' and 'metadata'
    """
    pass
```

### Formatting

```bash
# Auto-format
black src/

# Check style
flake8 src/
```

## 🐛 Reporting Bugs

Użyj GitHub Issues z template:

**Tytuł:** Krótki opis buga

**Opis:**

- Co się stało?
- Co powinno się stać?
- Kroki do reprodukcji
- Screenshoty (jeśli applicable)
- Wersja/environment

## 💡 Feature Requests

GitHub Issues z template:

**Tytuł:** [FEATURE] Nazwa funkcji

**Opis:**

- Problem do rozwiązania
- Proponowane rozwiązanie
- Alternatywy
- Use cases

## 📚 Documentation

Aktualizuj dokumentację przy każdej zmianie:

- README.md - główne info
- API_ENDPOINTS.md - nowe endpointy
- .env.example - nowe zmienne
- Inline comments - complex logic

## 🔒 Security

Znalazłeś lukę? **NIE** twórz publicznego issue!
Email: kontakt@novahouse.pl

## ❓ Questions

- GitHub Discussions
- Issues z tagiem `question`
- Email: kontakt@novahouse.pl

## 📜 License

Ten projekt używa [MIT License](LICENSE).

---

**Dziękujemy za Twój wkład! 🎉**
