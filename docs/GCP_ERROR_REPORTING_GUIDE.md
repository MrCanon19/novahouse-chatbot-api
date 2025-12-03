# 🔍 GCP Error Reporting - Kompletny Przewodnik

## 🎯 Czym jest GCP Error Reporting?

**DARMOWY** monitoring błędów wbudowany w Google Cloud Platform. Automatycznie zbiera i grupuje błędy z Twojego chatbota.

---

## 📊 Jak używać Error Reporting

### 1. **Otwórz Dashboard Błędów**

```
https://console.cloud.google.com/errors?project=glass-core-467907-e9
```

Lub w GCP Console:
```
Navigation Menu → Error Reporting → default (service)
```

---

### 2. **Co zobaczysz w Dashboard**

#### A) **Error Groups** (Zgrupowane błędy)
- Każdy typ błędu ma swoją grupę
- Widzisz ile razy wystąpił
- Pierwszy i ostatni raz wystąpienia
- Wykres częstotliwości

#### B) **Error Details** (Szczegóły błędu)
Po kliknięciu w błąd zobaczysz:
- **Stack trace** - dokładna linia kodu gdzie wystąpił błąd
- **Request details** - URL, metoda HTTP, IP użytkownika
- **Environment** - wersja aplikacji, timestamp
- **Similar errors** - inne powiązane błędy

---

## 🔔 Jak ustawić ALERTY (Email/SMS przy błędzie)

### **Krok 1: Utwórz Policy Alerting**

```bash
# W GCP Console
Navigation Menu → Monitoring → Alerting → Create Policy
```

### **Krok 2: Warunki alertu**

```yaml
Metric: Error Reporting
Condition: Error count > 5 in 5 minutes
Notification: Email lub SMS
```

### **Krok 3: Test**

```bash
# Wygeneruj testowy błąd
curl "https://glass-core-467907-e9.ey.r.appspot.com/test-error-404"
```

Dostaniesz email w ~2 minuty!

---

## 📈 Najczęstsze błędy które zobaczysz

### 1. **404 Not Found**
```
Użytkownik wszedł na nieistniejący URL
Nie wymaga naprawy - to normalne
```

### 2. **500 Internal Server Error**
```
🚨 KRYTYCZNY! Coś crashnęło w kodzie
Sprawdź stack trace i napraw
```

### 3. **Database Connection Error**
```
Cloud SQL nie odpowiada
Sprawdź czy instance działa: gcloud sql instances describe
```

### 4. **OpenAI API Error**
```
Brak klucza API lub limit exceeded
Sprawdź OPENAI_API_KEY w app.yaml
```

---

## 🛠️ Praktyczne przykłady debugowania

### **Przykład 1: Chatbot nie odpowiada**

1. Otwórz Error Reporting
2. Szukaj `chat` w filtrze
3. Zobacz stack trace:
   ```python
   File "/srv/src/routes/chatbot.py", line 123
   KeyError: 'message'
   ```
4. Napraw: Sprawdź czy request ma pole `message`

### **Przykład 2: Baza danych timeout**

1. Error Reporting pokaże:
   ```
   OperationalError: could not connect to server
   ```
2. Fix:
   ```bash
   # Sprawdź Cloud SQL
   gcloud sql instances describe novahouse-chatbot-db

   # Restart jeśli potrzeba
   gcloud sql instances restart novahouse-chatbot-db
   ```

### **Przykład 3: Out of Memory (OOM)**

1. Error Reporting:
   ```
   MemoryError: Cannot allocate memory
   ```
2. Fix: Zwiększ instance z F2 na F4
   ```yaml
   # app.yaml
   instance_class: F4  # 1 GB RAM zamiast 512 MB
   ```

---

## 🎓 Pro Tips

### **1. Filtrowanie błędów**

```
W Dashboard → Filters:
- Service: default
- Time range: Last 7 days
- Status: Open only
```

### **2. Ignorowanie znaných błędów**

```
Kliknij błąd → Mark as Resolved
(Nie będzie więcej alertować)
```

### **3. Łączenie z logami**

```
W Error Details → View Logs
(Przejdzie do pełnych logów tego błędu)
```

### **4. API Access (dla automatyzacji)**

```bash
# Lista błędów przez CLI
gcloud error-reporting events list \
  --service=default \
  --limit=10
```

---

## 📊 Monitoring Dashboard (dodatkowy)

Oprócz Error Reporting masz też:

### **Cloud Monitoring** (metryki)
```
https://console.cloud.google.com/monitoring?project=glass-core-467907-e9
```

Co pokazuje:
- ✅ CPU usage
- ✅ Memory usage
- ✅ Request count
- ✅ Latency
- ✅ Error rate %

### **Cloud Logging** (pełne logi)
```
https://console.cloud.google.com/logs?project=glass-core-467907-e9
```

Co pokazuje:
- ✅ Wszystkie print() z kodu
- ✅ HTTP requesty
- ✅ Gunicorn logi
- ✅ Database queries

---

## 🔥 Quick Actions (szybkie komendy)

### **Sprawdź błędy ostatniej godziny:**
```bash
gcloud error-reporting events list \
  --service=default \
  --time-range=1h
```

### **Zobacz logi z ostatniego deploy:**
```bash
gcloud app logs read --limit=50 --service=default
```

### **Sprawdź czy app żyje:**
```bash
curl https://glass-core-467907-e9.ey.r.appspot.com/health
```

### **Force restart app:**
```bash
# Deploy tej samej wersji = restart
gcloud app deploy app.yaml --quiet
```

---

## 💡 FAQ

**Q: Czy Error Reporting kosztuje?**  
A: NIE! Jest DARMOWY dla App Engine (do 5 GB logów/mc)

**Q: Jak długo są przechowywane błędy?**  
A: 30 dni (możesz exportować do BigQuery na dłużej)

**Q: Czy mogę dostać alert na Slack?**  
A: TAK! W Alerting Policy wybierz Slack webhook

**Q: Czy Error Reporting wymaga zmian w kodzie?**  
A: NIE! Działa automatycznie dla App Engine

**Q: Co jeśli mam zbyt dużo błędów 404?**  
A: Mark as Resolved lub dodaj filter w alertach

---

## 🎯 Podsumowanie

**Error Reporting to Twój najlepszy przyjaciel do debugowania:**

✅ **DARMOWY** - 0 zł/mc  
✅ **Automatyczny** - zero konfiguracji  
✅ **Szybki** - błędy widoczne w 10s  
✅ **Precyzyjny** - dokładna linia kodu  
✅ **Alerting** - email/SMS przy problemie  

**Zamiast Sentry ($26/mc) masz to samo DARMOWO! 🎉**

---

## 📚 Dodatkowe zasoby

- [GCP Error Reporting Docs](https://cloud.google.com/error-reporting/docs)
- [Alerting Guide](https://cloud.google.com/monitoring/alerts)
- [Log Explorer](https://cloud.google.com/logging/docs/view/logs-explorer-interface)

---

**Masz pytania?** Wszystkie błędy już logują się automatycznie! Sprawdź dashboard: https://console.cloud.google.com/errors?project=glass-core-467907-e9
