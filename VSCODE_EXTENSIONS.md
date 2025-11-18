# 🎨 Rekomendowane Rozszerzenia VSCode dla NovaHouse Chatbot

**Personalized for:** Michał Marini  
**Project:** NovaHouse Chatbot API  
**Date:** 18.11.2025

---

## 🔥 MUST HAVE (Zainstaluj najpierw)

### 1. **Python** (ms-python.python)

- **Dlaczego:** Base extension dla Python development
- **Features:** IntelliSense, debugging, linting, formatting
- **Priorytet:** ⭐⭐⭐⭐⭐ CRITICAL

### 2. **Pylance** (ms-python.vscode-pylance)

- **Dlaczego:** Szybszy IntelliSense, lepsze type checking
- **Features:** Auto-imports, type hints, docstrings
- **Priorytet:** ⭐⭐⭐⭐⭐ CRITICAL

### 3. **Docker** (ms-azuretools.vscode-docker)

- **Dlaczego:** Zarządzanie kontenerami z VSCode
- **Features:** Build/run containers, view logs, attach to containers
- **Priorytet:** ⭐⭐⭐⭐⭐ ESSENTIAL (masz docker-compose.yml)

### 4. **GitLens** (eamodio.gitlens)

- **Dlaczego:** Superpowers dla Git
- **Features:** Blame annotations, commit history, file history
- **Priorytet:** ⭐⭐⭐⭐⭐ ESSENTIAL

---

## 🚀 HIGH PRIORITY (Bardzo przydatne)

### 5. **Black Formatter** (ms-python.black-formatter)

- **Dlaczego:** Auto-formatowanie Python code
- **Setup:** Już skonfigurowane w settings.json (format on save)
- **Priorytet:** ⭐⭐⭐⭐

### 6. **Flake8** (ms-python.flake8)

- **Dlaczego:** Linting errors w czasie rzeczywistym
- **Setup:** Używa .flake8 config który masz
- **Priorytet:** ⭐⭐⭐⭐

### 7. **Better Comments** (aaron-bond.better-comments)

- **Dlaczego:** Kolorowe komentarze (TODO, FIXME, etc.)
- **Features:**
  ```python
  # TODO: Do this
  # FIXME: Fix this bug
  # ! IMPORTANT
  # ? Question
  # * Highlight
  ```
- **Priorytet:** ⭐⭐⭐⭐

### 8. **TODO Tree** (gruntfuggly.todo-tree)

- **Dlaczego:** Lista wszystkich TODO/FIXME w projekcie
- **Features:** Search, filter, badge counts
- **Priorytet:** ⭐⭐⭐⭐

### 9. **YAML** (redhat.vscode-yaml)

- **Dlaczego:** Validation dla docker-compose.yml, app.yaml, CI/CD
- **Features:** Auto-complete, schema validation
- **Priorytet:** ⭐⭐⭐⭐

### 10. **Error Lens** (usernamehw.errorlens)

- **Dlaczego:** Errors/warnings inline (nie musisz najeżdżać myszką)
- **Features:** Real-time error highlighting
- **Priorytet:** ⭐⭐⭐⭐

---

## 💡 RECOMMENDED (Nice to have)

### 11. **Markdown All in One** (yzhang.markdown-all-in-one)

- **Dlaczego:** Masz 45+ markdown files!
- **Features:** TOC, preview, shortcuts, formatting
- **Priorytet:** ⭐⭐⭐

### 12. **Code Spell Checker** (streetsidesoftware.code-spell-checker)

- **Dlaczego:** Catch typos w dokumentacji i komentarzach
- **Features:** Multi-language support (PL/EN)
- **Priorytet:** ⭐⭐⭐

### 13. **autoDocstring** (njpwerner.autodocstring)

- **Dlaczego:** Auto-generowanie Python docstrings
- **Features:** Google/NumPy/Sphinx formats
- **Usage:** Napisz `"""` i wciśnij Enter
- **Priorytet:** ⭐⭐⭐

### 14. **Python Test Explorer** (littlefoxteam.vscode-python-test-adapter)

- **Dlaczego:** UI dla pytest w sidebar
- **Features:** Run/debug tests z GUI, see results
- **Priorytet:** ⭐⭐⭐

### 15. **REST Client** (humao.rest-client)

- **Dlaczego:** Test API endpoints bez Postman
- **Features:** HTTP requests w .http files
- **Example:**

  ```http
  ### Health Check
  GET http://localhost:8080/api/health

  ### Chat
  POST http://localhost:8080/api/chat
  Content-Type: application/json

  {
    "message": "Witaj"
  }
  ```

- **Priorytet:** ⭐⭐⭐

---

## 🎯 SPECIALIZED (Dla konkretnych zadań)

### 16. **Database Client** (cweijan.vscode-database-client2)

- **Dlaczego:** Zarządzanie PostgreSQL z VSCode
- **Features:** Query editor, table explorer, export data
- **Priorytet:** ⭐⭐⭐

### 17. **Thunder Client** (rangav.vscode-thunder-client)

- **Dlaczego:** Lightweight Postman w VSCode
- **Features:** Collections, environments, scripting
- **Priorytet:** ⭐⭐

### 18. **GitHub Copilot** (github.copilot)

- **Dlaczego:** AI code completion
- **Cost:** $10/month (FREE for students/open source)
- **Features:** Całe funkcje, dokumentacja, testy
- **Priorytet:** ⭐⭐⭐⭐⭐ GAME CHANGER

### 19. **GitHub Copilot Chat** (github.copilot-chat)

- **Dlaczego:** Chat z AI bezpośrednio w VSCode
- **Features:** Explain code, refactor, write tests
- **Priorytet:** ⭐⭐⭐⭐

---

## 🌈 UI/UX ENHANCEMENTS

### 20. **Material Icon Theme** (pkief.material-icon-theme)

- **Dlaczego:** Lepsze ikony dla plików
- **Features:** Python, Docker, YAML, Markdown icons
- **Priorytet:** ⭐⭐

### 21. **Indent Rainbow** (oderwat.indent-rainbow)

- **Dlaczego:** Kolorowe indentacje (ułatwia czytanie Python)
- **Priorytet:** ⭐⭐

### 22. **Bracket Pair Colorizer 2** (DEPRECATED - built into VSCode)

- **Note:** Używaj built-in `editor.bracketPairColorization.enabled`

---

## 🔧 DEVOPS & MONITORING

### 23. **Kubernetes** (ms-kubernetes-tools.vscode-kubernetes-tools)

- **Dlaczego:** Jeśli przejdziesz z GCP App Engine na GKE
- **Priorytet:** ⭐ (future-proofing)

### 24. **Remote - SSH** (ms-vscode-remote.remote-ssh)

- **Dlaczego:** Edit files na GCP VM bezpośrednio
- **Priorytet:** ⭐⭐

### 25. **Remote - Containers** (ms-vscode-remote.remote-containers)

- **Dlaczego:** Develop inside Docker container
- **Priorytet:** ⭐⭐

---

## 📦 QUICK INSTALL COMMANDS

### Essential Pack (Top 10)

```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.black-formatter
code --install-extension ms-python.flake8
code --install-extension ms-azuretools.vscode-docker
code --install-extension eamodio.gitlens
code --install-extension aaron-bond.better-comments
code --install-extension gruntfuggly.todo-tree
code --install-extension redhat.vscode-yaml
code --install-extension usernamehw.errorlens
```

### Documentation Pack

```bash
code --install-extension yzhang.markdown-all-in-one
code --install-extension streetsidesoftware.code-spell-checker
code --install-extension davidanson.vscode-markdownlint
```

### Testing Pack

```bash
code --install-extension littlefoxteam.vscode-python-test-adapter
code --install-extension humao.rest-client
code --install-extension rangav.vscode-thunder-client
```

### AI Pack (Game Changer!)

```bash
code --install-extension github.copilot
code --install-extension github.copilot-chat
```

---

## ⚙️ RECOMMENDED SETTINGS

Dodaj do `.vscode/settings.json`:

```json
{
  // Error Lens
  "errorLens.enabled": true,
  "errorLens.delay": 500,

  // TODO Tree
  "todo-tree.general.tags": ["TODO", "FIXME", "HACK", "XXX", "NOTE"],
  "todo-tree.highlights.defaultHighlight": {
    "foreground": "black",
    "background": "yellow",
    "iconColour": "yellow"
  },

  // Copilot
  "github.copilot.enable": {
    "*": true,
    "yaml": true,
    "plaintext": false,
    "markdown": true
  },

  // Auto Save
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,

  // Bracket Pairs (built-in)
  "editor.bracketPairColorization.enabled": true,
  "editor.guides.bracketPairs": true,

  // Minimap
  "editor.minimap.enabled": true,
  "editor.minimap.maxColumn": 120
}
```

---

## 🎓 PRO TIPS

### 1. Command Palette Power

- **Cmd+Shift+P** (Mac) lub **Ctrl+Shift+P** (Windows)
- Type: `Python: Run All Tests` - uruchom wszystkie testy
- Type: `Docker: Compose Up` - start containers
- Type: `Git: Commit` - quick commit

### 2. Multi-Cursor Editing

- **Cmd+D** (Mac) - select next occurrence
- **Cmd+Shift+L** - select all occurrences
- **Alt+Click** - add cursor

### 3. Quick Fix

- **Cmd+.** - show quick fixes for errors
- Auto-import missing modules
- Auto-fix linting issues

### 4. Integrated Terminal

- **Ctrl+`** - toggle terminal
- **Cmd+Shift+`** - new terminal
- Run `make`, `pytest`, `docker-compose` directly

### 5. Split Editor

- **Cmd+\\** - split editor
- **Cmd+1/2/3** - focus split
- Perfect for: code + tests side-by-side

---

## 📊 EXTENSION PRIORITY SUMMARY

| Category               | Extensions                         | Priority   |
| ---------------------- | ---------------------------------- | ---------- |
| **Python Development** | Python, Pylance, Black, Flake8     | ⭐⭐⭐⭐⭐ |
| **Docker & DevOps**    | Docker, Kubernetes                 | ⭐⭐⭐⭐⭐ |
| **Git**                | GitLens                            | ⭐⭐⭐⭐⭐ |
| **Code Quality**       | Error Lens, TODO Tree              | ⭐⭐⭐⭐   |
| **Documentation**      | Markdown All in One, Spell Checker | ⭐⭐⭐     |
| **Testing**            | Python Test Explorer, REST Client  | ⭐⭐⭐     |
| **AI**                 | GitHub Copilot, Copilot Chat       | ⭐⭐⭐⭐⭐ |
| **UI/UX**              | Material Icons, Indent Rainbow     | ⭐⭐       |

---

## 🚀 RECOMMENDED INSTALL ORDER

### Week 1: Essentials

1. Python + Pylance
2. Docker
3. GitLens
4. Black Formatter + Flake8

### Week 2: Quality & Productivity

5. Error Lens
6. TODO Tree
7. Better Comments
8. YAML

### Week 3: Documentation & Testing

9. Markdown All in One
10. Code Spell Checker
11. Python Test Explorer
12. REST Client

### Week 4: Game Changers

13. **GitHub Copilot** 🤖
14. **GitHub Copilot Chat** 💬

---

## 💰 COST ANALYSIS

| Extension           | Cost       | Worth It?                     |
| ------------------- | ---------- | ----------------------------- |
| **Most extensions** | FREE ✅    | -                             |
| **GitHub Copilot**  | $10/month  | ⭐⭐⭐⭐⭐ Saves 30% time     |
| **Total**           | ~$10/month | ROI: ~10-20 hours saved/month |

**Student Discount:** GitHub Copilot FREE z GitHub Student Developer Pack!

---

## 🎯 FINAL RECOMMENDATIONS (Top 5)

Jeśli możesz zainstalować tylko 5:

1. **Python + Pylance** - Base development
2. **Docker** - Container management
3. **GitLens** - Git superpowers
4. **Error Lens** - Real-time error feedback
5. **GitHub Copilot** - AI assistant (GAME CHANGER!)

---

**Created for:** NovaHouse Chatbot API v2.3.0  
**Last Updated:** 18.11.2025  
**Maintained by:** Michał Marini

🎉 Happy Coding with superpowers!
