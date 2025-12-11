# 🔧 Naprawa terminala - Problem z cudzysłowami

## ⚠️ Problem

Jeśli widzisz w terminalu:
```
dquote> 
```

To znaczy, że masz **otwarty cudzysłów** - terminal czeka na zamknięcie.

## ✅ Rozwiązanie

### Opcja 1: Zamknij cudzysłów i anuluj

Naciśnij `Ctrl+C` (anuluje komendę)

### Opcja 2: Zamknij cudzysłów i wykonaj

Naciśnij `Enter` (zamknie cudzysłów i spróbuje wykonać komendę)

---

## 🚀 Poprawne użycie skryptu

### ❌ BŁĘDNIE (brakuje zamknięcia cudzysłowu):
```bash
./scripts/quick_commit_no_hooks.sh "Aktualizacja kodu
```

### ✅ POPRAWNIE (zamknięty cudzysłów):
```bash
./scripts/quick_commit_no_hooks.sh "Aktualizacja kodu"
```

---

## 💡 Najprostszy sposób (bez cudzysłowów)

```bash
cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api"
./scripts/quick_commit_no_hooks.sh Aktualizacja kodu
```

**Uwaga:** Jeśli wiadomość ma spacje, użyj cudzysłowów:
```bash
./scripts/quick_commit_no_hooks.sh "Aktualizacja kodu"
```

---

## 🎯 Szybka komenda (jedna linia)

```bash
cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api" && ./scripts/quick_commit_no_hooks.sh "Aktualizacja kodu"
```

---

## 📋 Jeśli nadal masz problem

1. Naciśnij `Ctrl+C` (anuluj)
2. Wpisz: `cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api"`
3. Wpisz: `./scripts/quick_commit_no_hooks.sh "Aktualizacja kodu"`

---

## ✅ Alternatywa - bez skryptu

```bash
cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api"
git add .
git commit --no-verify -am "Aktualizacja kodu"
git push
```

