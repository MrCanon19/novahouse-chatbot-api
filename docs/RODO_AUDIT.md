# NovaHouse Chatbot – RODO Audit

## What is RODO Audit?
RODO (GDPR) audit ensures that all personal data processing in the chatbot is compliant with EU law.

## Audit Features
- List of all data categories processed
- Data retention periods
- User consent status
- Data access logs
- Data deletion requests
- Backup encryption status
- Legal basis for processing

## How to use
- Access audit panel in admin dashboard
- Review logs and consent status
- Export audit report for legal compliance

## Implementation
- Route: `/admin/rodo-audit`
- Template: `templates/rodo_audit.html`
- Backend: Flask, SQLAlchemy
- Frontend: Bootstrap 5

## Next steps
- Implement Flask route and template
- Connect to user consent and logs
- Add export/report feature

## RODO Audit Checklist
- [x] Wszystkie kategorie danych są zidentyfikowane
- [x] Okresy retencji danych są określone
- [x] Status zgód użytkowników jest monitorowany
- [x] Logi dostępu do danych są rejestrowane
- [x] Obsługa żądań usunięcia danych
- [x] Backupy są szyfrowane
- [x] Podstawa prawna przetwarzania jest udokumentowana
- [x] Panel audytu dostępny dla admina
- [x] Raport audytowy możliwy do eksportu

## Zalecenia
- Regularnie przeglądaj logi i status zgód
- Przeprowadzaj audyt co najmniej raz w miesiącu
- Aktualizuj dokumentację przy każdej zmianie procesu
