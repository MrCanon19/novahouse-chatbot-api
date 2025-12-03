# 🔥 Usuwanie Sekretów z Historii Git

## ⚠️ KRYTYCZNE: Sekret w 18 commitach

`app.yaml` z produkcyjnymi sekretami został wykryty w 18 commitach:
- **OpenAI API Key** - dostęp do modeli GPT
- **Monday.com API Token** - dostęp do CRM
- **PostgreSQL Password** - dostęp do bazy danych
- **SECRET_KEY** - Flask session signing
- **API_KEY** - autentykacja API

## 🚨 Co Musisz Zrobić NATYCHMIAST

### Krok 1: Stwórz Backup (już wykonane)
```bash
git branch backup-before-purge
git push origin backup-before-purge
```

### Krok 2: Uruchom Skrypt Czyszczący
```bash
cd /Users/michalmarini/Projects/manus/novahouse-chatbot-api
./scripts/purge_secrets_from_history.sh
```

**Skrypt zrobi:**
1. ✅ Zapyta o potwierdzenie (wymaga wpisania "YES")
2. ✅ Stworzy lokalny backup w `../backup-$(date +%Y%m%d-%H%M%S)`
3. ✅ Uruchomi BFG Repo Cleaner do usunięcia `app.yaml` z CAŁEJ historii
4. ✅ Wyczyści reflog i garbage collection
5. ✅ Pokaże instrukcje force push

### Krok 3: Force Push (WYMAGA UWAGI!)
```bash
git push --force --all origin
git push --force --tags origin
```

### Krok 4: Rotacja Wszystkich Sekretów
**MUSISZ to zrobić, bo klucze są już wyciekło publicznie!**

```bash
# Wygeneruj nowe sekret
python3 scripts/generate_credentials.py

# Zaktualizuj GCP Secrets Manager
# (instrukcje w docs/INSTRUKCJA_GCP_SECRETS.md)
```

### Krok 5: Powiadom Zespół
**WSZYSCY MUSZĄ zrobić fresh clone!**

```bash
# Stary sposób (NIE DZIAŁA po force push):
git pull

# Poprawny sposób:
cd ..
rm -rf novahouse-chatbot-api
git clone git@github.com:OWNER/novahouse-chatbot-api.git
```

## 📋 Jakie Commity Zawierają Sekrety

```bash
# Lista 18 commitów z app.yaml (najstarsze → najnowsze):
d9a9be4 - fix: Remove leaked credentials from git tracking
c91f345 - fix: Improve error logging in RODO audit operations
2971b9f - docs: Add comprehensive audit reports (security, quality, database, dependencies)
987cd2e - Finalny commit przed wysłaniem na GitHub
# ... (pozostałe 14 commitów)
```

## 🔒 Jak Zapobiec w Przyszłości

1. ✅ **Już zrobione:**
   - `app.yaml` dodany do `.gitignore`
   - `app.yaml.example` jako template bez sekretów
   - Pre-commit hooks sprawdzające sekrety

2. 🔄 **Musisz zrobić:**
   - Przenieś wszystkie sekrety do GCP Secrets Manager
   - Używaj `app.yaml.example` → kopiuj do `app.yaml` lokalnie
   - **NIGDY** nie commituj `app.yaml`

## 🆘 Pomoc i Wsparcie

Jeśli coś pójdzie nie tak podczas force push:
```bash
# Przywróć z backupu
git reset --hard backup-before-purge
```

Jeśli zespół ma problemy po force push:
```bash
# Każdy członek musi:
git fetch origin
git reset --hard origin/main
# LUB zrobić fresh clone (bezpieczniejsze)
```

## ✅ Weryfikacja Sukcesu

Po purge sprawdź:
```bash
# Czy app.yaml zniknął z historii:
git log --all --full-history --oneline -- app.yaml
# (powinno być PUSTE)

# Czy obecny commit nie ma app.yaml:
git ls-files | grep app.yaml
# (powinno być PUSTE)

# Czy example jest:
git ls-files | grep app.yaml.example
# app.yaml.example ✅
```

## 📊 Status Realizacji

- [x] Analiza historii git (18 commitów wykrytych)
- [x] Instalacja BFG Repo Cleaner
- [x] Stworzenie skryptu purge
- [ ] **← TERAZ:** Wykonanie purge
- [ ] Force push do GitHub
- [ ] Rotacja wszystkich sekretów
- [ ] Powiadomienie zespołu
- [ ] Fresh clone przez wszystkich

---

**Utworzone:** 2025-12-20  
**Priorytet:** 🔥 KRYTYCZNY - DO NATYCHMIASTOWEJ REALIZACJI  
**Szacowany czas:** 15-30 minut (+ czas na koordynację zespołu)
