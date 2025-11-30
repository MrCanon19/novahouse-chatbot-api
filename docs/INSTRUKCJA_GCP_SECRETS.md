# Instrukcja: Sekrety GCP dla CI/CD

Aby automatyczne wdrożenia na Google Cloud App Engine działały poprawnie, musisz ustawić dwa sekrety w repozytorium GitHub:

1. **GCP_SA_KEY**
   - Wartość: JSON z kluczem serwisowym Google Cloud (Service Account Key)
   - Jak uzyskać: W Google Cloud Console wygeneruj klucz dla konta serwisowego z uprawnieniami do wdrożenia App Engine.
   - Jak dodać: Settings → Secrets → Actions → New repository secret → Nazwa: `GCP_SA_KEY`, wartość: wklej JSON.

2. **GCP_PROJECT_ID**
   - Wartość: ID projektu Google Cloud (np. `glass-core-467907`)
   - Jak uzyskać: W Google Cloud Console znajdziesz Project ID na stronie projektu.
   - Jak dodać: Settings → Secrets → Actions → New repository secret → Nazwa: `GCP_PROJECT_ID`, wartość: wklej ID projektu.

## Przykład
- `GCP_SA_KEY`: `{ "type": "service_account", ... }`
- `GCP_PROJECT_ID`: `glass-core-467907`

Po ustawieniu tych sekretów pipeline CI/CD automatycznie wdroży aplikację na GCP App Engine.

---

**Jeśli napotkasz błąd autoryzacji lub wdrożenia, sprawdź czy oba sekrety są poprawnie ustawione!**
