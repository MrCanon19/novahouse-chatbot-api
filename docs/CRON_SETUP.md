# Cron Configuration Guide

## Aktywne zadania cron:

### 1. Auto-push do GitHub (co 30 minut)

```bash
*/30 * * * * /Users/michalmarini/Projects/manus/novahouse-chatbot-api/auto_push.sh
```

### 2. Monitoring crona (co godzinę)

```bash
0 * * * * /Users/michalmarini/Projects/manus/novahouse-chatbot-api/scripts/monitor_cron.sh
```

## Instalacja:

1. Otwórz edytor crontab:

```bash
crontab -e
```

2. Dodaj obie linie na końcu pliku

3. Zapisz i zamknij edytor (w nano: Ctrl+O, Enter, Ctrl+X)

## Sprawdzanie statusu:

### Lista aktywnych zadań:

```bash
crontab -l
```

### Sprawdź logi auto-push:

```bash
tail -f ~/Projects/manus/novahouse-chatbot-api/logs/auto_push.log
```

### Sprawdź alerty monitoringu:

```bash
tail -f ~/Projects/manus/novahouse-chatbot-api/logs/cron_alerts.log
```

## Zmiana częstotliwości:

- **Co 15 minut**: `*/15 * * * *`
- **Co godzinę**: `0 * * * *`
- **Co 2 godziny**: `0 */2 * * *`
- **Codziennie o 9:00**: `0 9 * * *`
- **W dni robocze o 18:00**: `0 18 * * 1-5`

## Wyłączenie crona:

```bash
crontab -e
# Usuń odpowiednie linie lub dodaj # na początku, aby je zakomentować
```

## Testowanie ręczne:

```bash
# Test auto-push
/Users/michalmarini/Projects/manus/novahouse-chatbot-api/auto_push.sh

# Test monitoringu
/Users/michalmarini/Projects/manus/novahouse-chatbot-api/scripts/monitor_cron.sh
```
