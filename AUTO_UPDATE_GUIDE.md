# 🤖 Automatyczne Generowanie Aktualizacji

System do automatycznego tworzenia plików z aktualizacjami projektu po każdym deploy'u.

---

## 🎯 Dostępne Opcje

### 1. **Ręczne Generowanie** (Polecane)

Po każdym deploy'u uruchom:

```bash
./generate-update.sh
```

To utworzy plik `updates/AKTUALIZACJA_YYYYMMDD_V{wersja}.md` z:

- ✅ Informacjami o commit'cie
- ✅ Zmienionymi plikami
- ✅ Ostatnimi 5 commit'ami
- ✅ Checklist'ą do uzupełnienia
- ✅ Metrykami wydajności

**Zalety:**

- Pełna kontrola nad tym kiedy generujesz aktualizację
- Możesz od razu uzupełnić checklist'y
- Nie generuje zbędnych plików

---

### 2. **Automatyczny Hook** (Zaawansowane)

Jeśli chcesz **całkowicie automatycznego** generowania po każdym commit z zmianami w plikach deploy'owych:

```bash
# Instalacja hooka
cp auto-update-hook.sh .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```

**Monitorowane pliki:**

- `app.yaml`
- `requirements.txt`
- `src/*`
- `main.py`

**Zalety:**

- Zero ręcznej pracy
- Nigdy nie zapomnisz wygenerować aktualizacji

**Wady:**

- Generuje aktualizacje automatycznie (możesz mieć ich więcej)
- Wymaga ręcznego uzupełnienia później

---

### 3. **Integracja z Deploy'em**

Dodaj do końca swojego procesu deploy'u w `cloudbuild.yaml` lub w skrypcie deploy'owym:

```yaml
# cloudbuild.yaml
steps:
  # ... Twoje kroki deploy'u ...

  - name: "gcr.io/cloud-builders/gcloud"
    entrypoint: "bash"
    args:
      - "-c"
      - |
        ./generate-update.sh
        git add updates/
        git commit -m "Docs: Auto-update po deploy'u" || true
        git push origin main || true
```

---

## 📋 Przykładowy Wygenerowany Plik

```markdown
# 🚀 Aktualizacja Projektu NovaHouse Chatbot

**Wersja:** 2.3.0  
**Data deployment:** 18.11.2025 19:45  
**Commit:** a1b2c3d

## ✅ Status Komponentów

- [x] Backend API
- [x] Frontend (Chatbot)
      ...
```

---

## 🔧 Customizacja

Możesz edytować `generate-update.sh` aby:

- Zmienić format pliku
- Dodać więcej informacji
- Zmienić lokalizację plików
- Dostosować checklist'y

---

## 💡 Polecana Metoda

**Dla małego zespołu:** Użyj **Opcji 1** (ręczne generowanie)

- Uruchamiaj `./generate-update.sh` po ważnych deploy'ach
- Uzupełniaj checklist'y od razu
- Commit'uj razem z deploy'em

**Dla większego zespołu:** Użyj **Opcji 3** (integracja z CI/CD)

- Automatyczne generowanie przy każdym deploy'u na produkcję
- Uzupełnianie checklist'y w review process

---

**Utworzono:** 18.11.2025  
**Autor:** NovaHouse Team
