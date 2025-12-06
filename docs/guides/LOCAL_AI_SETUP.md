# 🤖 Local AI Setup - Ollama + Continue + Qwen

Konfiguracja lokalnego asystenta AI dla tego projektu używając **Ollama** z modelem **Qwen2.5-coder:7b**.

## ✅ Status - GOTOWE DO UŻYCIA!

- ✅ Ollama zainstalowana
- ✅ Model `qwen2.5-coder:7b` pobrany (4.7 GB)
- ✅ Model `nomic-embed-text` pobrany (274 MB) - dla embeddings
- ✅ Serwer Ollama działa na `localhost:11434`
- ✅ Continue skonfigurowane w `~/.continue/config.json`
- ✅ Context providers włączone (code, docs, diff, terminal, problems, folder, codebase)
- ✅ Przykładowe prompty w `.vscode/continue-prompts.md`

**🎉 Wszystko gotowe - otwórz VS Code i naciśnij `Cmd+L` żeby zacząć!**

## 🚀 Quick Start

### 1. Sprawdź status Ollama

```bash
# Lista modeli
ollama list

# Test modelu
ollama run qwen2.5-coder:7b "Write a hello world in Python"
```

### 2. VS Code - Continue Extension

1. Zainstaluj rozszerzenie **Continue** w VS Code
2. Konfiguracja jest już gotowa w `.vscode/continue_config.json`
3. Otwórz panel Continue: `Cmd+L` (Mac) lub `Ctrl+L` (Windows/Linux)
4. Zacznij zadawać pytania o kod!

### 3. Przykłady użycia

**W panelu Continue możesz pisać:**

- "Wyjaśnij co robi funkcja `process_chat_message` w `src/routes/chatbot.py`"
- "Dodaj nowy endpoint `/api/stats` który zwraca statystyki leadów"
- "Znajdź wszystkie места gdzie używamy OpenAI API"
- "Napisz testy dla `src/routes/backup.py`"
- "Zrefaktoruj funkcję `run_auto_migration` żeby była bardziej czytelna"

**Tab autocomplete:**
- Zaczyna pisać kod, model automatycznie podpowiada dalszy ciąg
- Naciśnij `Tab` żeby zaakceptować podpowiedź

## 🔧 Zaawansowane

### Restart serwera Ollama

```bash
# Jeśli coś nie działa, zrestartuj serwer
pkill ollama
ollama serve > /dev/null 2>&1 &
```

### Zmiana modelu

Możesz użyć innych modeli, np.:

```bash
# Mniejszy, szybszy model
ollama pull qwen2.5-coder:1.5b

# Większy, dokładniejszy model
ollama pull qwen2.5-coder:32b
```

Następnie zmień w `.vscode/continue_config.json`:
```json
{
  "model": "qwen2.5-coder:1.5b"
}
```

### Context Providers

Konfiguracja włącza automatyczne pobieranie kontekstu z:
- ✅ **code** - aktualnie otwarty kod
- ✅ **docs** - dokumentacja projektu
- ✅ **diff** - niezatwierdzone zmiany git
- ✅ **terminal** - output z terminala
- ✅ **problems** - błędy i ostrzeżenia
- ✅ **folder** - struktura folderów
- ✅ **codebase** - przeszukiwanie całego repo

## 📊 Model Info

**Qwen2.5-coder:7b**
- Rozmiar: 4.7 GB
- Parametry: 7.6B
- Kwantyzacja: Q4_K_M (zoptymalizowana dla szybkości)
- Specjalizacja: Programowanie (Python, JavaScript, Go, Rust, itp.)
- Działa 100% lokalnie (bez internetu, bez kosztów API)

## 🆘 Troubleshooting

### Ollama nie odpowiada

```bash
# Sprawdź czy serwer działa
curl http://localhost:11434/api/tags

# Jeśli nie, uruchom:
ollama serve
```

### Model wolno generuje

- Użyj mniejszego modelu: `qwen2.5-coder:1.5b`
- Zamknij inne aplikacje żeby zwolnić RAM
- Model korzysta z GPU jeśli dostępne (M1/M2 Mac automatycznie)

### Continue nie widzi modelu

1. Sprawdź czy Ollama działa: `ollama list`
2. Przeładuj VS Code: `Cmd+Shift+P` → "Reload Window"
3. Sprawdź logi Continue: `Cmd+Shift+P` → "Continue: Show Logs"

## 🔗 Więcej info

- [Ollama Docs](https://ollama.com/library/qwen2.5-coder)
- [Continue Docs](https://docs.continue.dev/)
- [Qwen2.5-coder GitHub](https://github.com/QwenLM/Qwen2.5-Coder)

---

**Notatka:** Ten setup jest już skonfigurowany dla tego projektu. Po zainstalowaniu rozszerzenia Continue w VS Code wszystko powinno działać automatycznie! 🎉
