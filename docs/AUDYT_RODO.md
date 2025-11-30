# Audyt RODO i zgodności

Projekt NovaHouse Chatbot spełnia wymagania RODO oraz AI Act:
- Dane użytkowników są szyfrowane i przechowywane wyłącznie w chmurze GCP.
- Dostęp do danych mają wyłącznie uprawnieni administratorzy.
- Każdy użytkownik może zażądać eksportu lub usunięcia swoich danych (endpoint `/rodo/export`).
- System informuje o przetwarzaniu danych i wymaga zgody (panel RODO w czacie).
- Klucze API i sekrety są przechowywane wyłącznie w repozytorium GitHub jako sekrety.
- Backupy są szyfrowane i dostępne tylko dla administratorów.

## Checklist audytowa
- [x] Szyfrowanie danych w bazie i backupach
- [x] Panel zgody RODO i informacja o przetwarzaniu
- [x] Eksport/usuwanie danych na żądanie
- [x] Ograniczony dostęp do danych (role, uprawnienia)
- [x] Monitoring i alerty bezpieczeństwa
- [x] Dokumentacja procesów przetwarzania

## Zalecenia
- Regularna rotacja kluczy API i backupów
- Audyt uprawnień administratorów co 6 miesięcy
- Aktualizacja dokumentacji RODO przy każdej zmianie procesu

W razie pytań lub potrzeby audytu prawnego – kontakt z zespołem NovaHouse.
