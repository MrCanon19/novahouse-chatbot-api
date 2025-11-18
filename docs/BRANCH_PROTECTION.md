# Branch Protection Rules

Aby włączyć branch protection dla `main`:

1. Przejdź do **Settings** → **Branches** w repozytorium GitHub
2. Kliknij **Add rule**
3. Wpisz `main` w Branch name pattern
4. Zaznacz:
   - ✅ **Require a pull request before merging**
   - ✅ **Require approvals** (min. 1)
   - ✅ **Require status checks to pass before merging**
     - Wybierz: `test`, `lint`, `security-scan`
   - ✅ **Require branches to be up to date before merging**
   - ✅ **Do not allow bypassing the above settings**
5. Kliknij **Create**

## Workflow dla pracy z protected branch:

```bash
# Utwórz feature branch
git checkout -b feature/new-feature

# Wprowadź zmiany i commituj
git add .
git commit -m "Add new feature"

# Wypchnij branch
git push origin feature/new-feature

# Utwórz Pull Request na GitHub
# Poczekaj na review i zatwierdzenie
# Zmerguj przez GitHub UI
```

## Dodatkowe opcje (opcjonalne):

- **Require linear history** - wymusza rebase zamiast merge commits
- **Require signed commits** - wymaga GPG podpisów
- **Include administrators** - reguły dotyczą także adminów
