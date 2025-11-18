# Instrukcja Poprawki - Chatbot NovaHouse

## Problem
Aplikacja chatbota NovaHouse wdrożona na Google App Engine zwracała błąd 500 Internal Server Error z powodu braku pliku bazy danych `app.db` na serwerze.

## Przyczyna
Plik `.gcloudignore` zawierał regułę `*.db`, która blokowała przesyłanie pliku bazy danych SQLite podczas wdrażania na Google Cloud Platform.

## Rozwiązanie
Dodano wyjątek w pliku `.gcloudignore` dla konkretnego pliku bazy danych:

```
!src/database/app.db
```

Ta zmiana zapewnia, że plik `app.db` zostanie uwzględniony w paczce wdrożeniowej, mimo ogólnej reguły ignorującej pliki `.db`.

## Zmiany w kodzie
1. **Plik `.gcloudignore`** - dodano linię `!src/database/app.db` na końcu pliku
2. Pozostały kod aplikacji nie wymagał zmian

## Instrukcja wdrożenia
1. Rozpakuj załączony plik `novahouse_chatbot_fixed.zip`
2. Wdróż aplikację na Google App Engine używając standardowej procedury:
   ```bash
   gcloud app deploy app.yaml
   ```

## Weryfikacja
Po wdrożeniu aplikacja powinna działać poprawnie pod adresem:
https://glass-core-467907-e9.appspot.com/static/chatbot.html

Błąd 500 Internal Server Error nie powinien już występować przy wysyłaniu wiadomości do chatbota.

