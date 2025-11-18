# 🔒 Polityka Bezpieczeństwa

## 📊 Zgłaszanie Luk w Zabezpieczeniach

NovaHouse traktuje bezpieczeństwo bardzo poważnie. Jeśli odkryłeś lukę w zabezpieczeniach, prosimy o odpowiedzialne zgłoszenie.

### ✉️ Jak zgłosić?

**NIE** twórz publicznego Issue na GitHubie dla problemów bezpieczeństwa.

Zamiast tego:
1. Wyślij email na: **security@novahouse.pl**
2. Dołącz szczegółowy opis problemu
3. Dodaj kroki reprodukcji (jeśli możliwe)
4. Podaj swoją ocenę powagi (Critical/High/Medium/Low)

### ⏰ Czas odpowiedzi

- **Potwierdzenie otrzymania:** 24 godziny
- **Wstępna ocena:** 72 godziny  
- **Plan naprawy:** 7 dni (dla krytycznych luk)
- **Publikacja patcha:** Zależy od powagi (1-30 dni)

### 🎁 Program Bug Bounty

Obecnie nie mamy formalnego programu bug bounty, ale doceniamy odpowiedzialne zgłaszanie:
- Publiczne uznanie (jeśli chcesz)
- Wymienienie w CHANGELOG.md
- Darmowa konsultacja z zespołem (1h)

### 🛡️ Wspierane Wersje

| Wersja | Wsparcie Bezpieczeństwa |
|--------|-------------------------|
| 2.3.x  | ✅ Pełne wsparcie       |
| 2.2.x  | ⚠️ Krytyczne patche     |
| 2.1.x  | ❌ EOL                  |
| < 2.0  | ❌ EOL                  |

### 🔍 Znane Problemy

Aktualne znane problemy bezpieczeństwa:
- Brak (ostatnia aktualizacja: 18.11.2025)

### 🎯 Zakres

**W zakresie:**
- Injection (SQL, NoSQL, Command, Code)
- Broken Authentication
- Sensitive Data Exposure
- XXE (XML External Entities)
- Broken Access Control
- Security Misconfiguration
- XSS (Cross-Site Scripting)
- Insecure Deserialization
- Using Components with Known Vulnerabilities
- Insufficient Logging & Monitoring

**Poza zakresem:**
- DoS/DDoS attacks
- Social engineering
- Physical security
- Spam lub phishing niezwiązane z aplikacją

### 📜 Polityka Odpowiedzialnego Ujawniania

Po zgłoszeniu luki:
1. Nie ujawniaj publicznie do czasu patcha
2. Nie exploituj luki (tylko PoC)
3. Nie naruszaj prywatności użytkowników
4. Współpracuj z nami w dobrej wierze

### 🏆 Hall of Fame

Podziękowania dla:
- _Miejsce na pierwszego reportera_ 🥇

### 📚 Zasoby Bezpieczeństwa

- [SECURITY.md](./SECURITY.md) - Konfiguracja bezpieczeństwa
- [RODO_IMPLEMENTATION.md](./RODO_IMPLEMENTATION.md) - GDPR compliance
- [ROTATE_CREDENTIALS.md](./ROTATE_CREDENTIALS.md) - Rotacja secrets

### 📞 Kontakt

**Email bezpieczeństwa:** security@novahouse.pl  
**Team lead:** Michał Marini (@MrCanon19)  
**Response time:** 24h (weekdays), 48h (weekends)

---

**PGP Key Fingerprint:** _TBD_  
**Last Updated:** 18 listopada 2025
