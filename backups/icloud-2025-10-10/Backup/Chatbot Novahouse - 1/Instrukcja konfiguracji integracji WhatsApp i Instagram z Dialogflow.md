# Instrukcja konfiguracji integracji WhatsApp i Instagram z Dialogflow

## Integracja WhatsApp z Dialogflow

### 1. Przygotowanie konta WhatsApp Business API

#### 1.1. Rejestracja i weryfikacja konta WhatsApp Business
- Przejdź do [WhatsApp Business Platform](https://business.whatsapp.com/)
- Wybierz opcję "Rozpocznij" lub "Get Started"
- Zaloguj się na konto Facebook Business
- Wybierz lub utwórz aplikację Facebook dla WhatsApp
- Przejdź przez proces weryfikacji biznesowej (wymagane dokumenty firmowe NovaHouse)

#### 1.2. Wybór dostawcy WhatsApp Business API
Rekomendowane opcje:
- **Twilio** - łatwa integracja, dobre wsparcie, umiarkowane ceny
- **MessageBird** - prosta konfiguracja, dobra dokumentacja
- **360dialog** - popularne w Europie, dobre wsparcie dla języka polskiego

#### 1.3. Konfiguracja numeru telefonu
- Zweryfikuj numer telefonu firmowego
- Skonfiguruj nazwę profilu biznesowego i opis
- Dodaj logo firmy i informacje kontaktowe
- Przygotuj wiadomość powitania

#### 1.4. Uzyskanie dostępu do API
- Uzyskaj klucze API od wybranego dostawcy
- Skonfiguruj webhooks dla przychodzących wiadomości
- Ustaw adres URL dla powiadomień

### 2. Implementacja integracji WhatsApp z Dialogflow

#### 2.1. Utworzenie serwera pośredniczącego (middleware)
```javascript
// Przykładowy kod dla Node.js z Express
const express = require('express');
const bodyParser = require('body-parser');
const { SessionsClient } = require('@google-cloud/dialogflow');
const app = express();

app.use(bodyParser.json());

// Obsługa wiadomości przychodzących z WhatsApp
app.post('/webhook', async (req, res) => {
  const message = req.body.message;
  const sender = req.body.sender;
  
  // Wywołanie Dialogflow
  const sessionClient = new SessionsClient();
  const sessionPath = sessionClient.projectAgentSessionPath(
    'novahouse-chatbot', // ID projektu GCP
    sender, // ID sesji (numer telefonu nadawcy)
  );
  
  const request = {
    session: sessionPath,
    queryInput: {
      text: {
        text: message,
        languageCode: 'pl',
      },
    },
  };
  
  // Uzyskanie odpowiedzi z Dialogflow
  const responses = await sessionClient.detectIntent(request);
  const result = responses[0].queryResult;
  
  // Wysłanie odpowiedzi do WhatsApp
  await sendWhatsAppMessage(sender, result.fulfillmentText);
  
  res.status(200).send('OK');
});

// Funkcja wysyłająca odpowiedź do WhatsApp
async function sendWhatsAppMessage(recipient, message) {
  // Kod specyficzny dla wybranego dostawcy API WhatsApp
  // np. dla Twilio:
  const client = require('twilio')(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);
  await client.messages.create({
    body: message,
    from: 'whatsapp:+NUMER_TELEFONU_NOVAHOUSE',
    to: `whatsapp:${recipient}`
  });
}

app.listen(3000, () => console.log('Serwer nasłuchuje na porcie 3000'));
```

#### 2.2. Konfiguracja webhooków
- Wdróż serwer pośredniczący na platformie hostingowej (np. Google Cloud Run, Heroku)
- Skonfiguruj adres URL webhooków w panelu dostawcy WhatsApp Business API
- Ustaw odpowiednie zabezpieczenia (tokeny weryfikacyjne, HTTPS)

#### 2.3. Mapowanie odpowiedzi Dialogflow na format WhatsApp
- Skonfiguruj formatowanie odpowiedzi tekstowych
- Dodaj obsługę przycisków szybkiej odpowiedzi
- Zaimplementuj obsługę załączników (obrazy, dokumenty)

#### 2.4. Konfiguracja szablonów wiadomości WhatsApp
- Przygotuj szablony dla powiadomień inicjowanych przez system
- Złóż wnioski o zatwierdzenie szablonów (proces może trwać do 5 dni roboczych)
- Zaimplementuj mechanizm wyboru odpowiedniego szablonu

### 3. Testowanie integracji WhatsApp

#### 3.1. Testy podstawowe
- Sprawdź rozpoznawanie prostych intencji
- Przetestuj odpowiedzi na standardowe pytania
- Sprawdź obsługę kontekstu rozmowy

#### 3.2. Testy zaawansowane
- Przetestuj obsługę złożonych scenariuszy konwersacji
- Sprawdź obsługę załączników i multimediów
- Przetestuj mechanizm przekazywania rozmowy do konsultanta

#### 3.3. Testy wydajnościowe
- Sprawdź czas odpowiedzi
- Przetestuj zachowanie przy wielu równoczesnych rozmowach
- Zweryfikuj limity API i potencjalne ograniczenia

## Integracja Instagram z Dialogflow

### 1. Przygotowanie konta Instagram Business

#### 1.1. Konfiguracja konta biznesowego
- Przekształć konto Instagram NovaHouse na konto biznesowe (jeśli jeszcze nie jest)
- Połącz konto Instagram z Facebook Page
- Dodaj konto do Facebook Business Manager

#### 1.2. Konfiguracja Facebook Developer Account
- Utwórz lub użyj istniejącego konta Facebook Developer
- Utwórz nową aplikację Facebook dla Instagram Messaging
- Dodaj produkt "Messenger Platform" do aplikacji
- Uzyskaj niezbędne klucze API i tokeny dostępu

### 2. Implementacja integracji Instagram z Dialogflow

#### 2.1. Konfiguracja webhooków Facebook Messenger
```javascript
// Przykładowy kod dla Node.js z Express
const express = require('express');
const bodyParser = require('body-parser');
const { SessionsClient } = require('@google-cloud/dialogflow');
const app = express();

app.use(bodyParser.json());

// Weryfikacja webhooków Facebook
app.get('/webhook', (req, res) => {
  const VERIFY_TOKEN = process.env.FB_VERIFY_TOKEN;
  
  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];
  
  if (mode && token === VERIFY_TOKEN) {
    res.status(200).send(challenge);
  } else {
    res.sendStatus(403);
  }
});

// Obsługa wiadomości przychodzących z Instagram
app.post('/webhook', async (req, res) => {
  const body = req.body;
  
  if (body.object === 'instagram') {
    for (const entry of body.entry) {
      for (const messaging of entry.messaging) {
        const sender = messaging.sender.id;
        
        if (messaging.message && messaging.message.text) {
          const message = messaging.message.text;
          
          // Wywołanie Dialogflow
          const sessionClient = new SessionsClient();
          const sessionPath = sessionClient.projectAgentSessionPath(
            'novahouse-chatbot', // ID projektu GCP
            `instagram-${sender}`, // ID sesji
          );
          
          const request = {
            session: sessionPath,
            queryInput: {
              text: {
                text: message,
                languageCode: 'pl',
              },
            },
          };
          
          // Uzyskanie odpowiedzi z Dialogflow
          const responses = await sessionClient.detectIntent(request);
          const result = responses[0].queryResult;
          
          // Wysłanie odpowiedzi do Instagram
          await sendInstagramMessage(sender, result.fulfillmentText);
        }
      }
    }
    res.status(200).send('OK');
  } else {
    res.sendStatus(404);
  }
});

// Funkcja wysyłająca odpowiedź do Instagram
async function sendInstagramMessage(recipient, message) {
  const axios = require('axios');
  
  await axios.post(
    `https://graph.facebook.com/v17.0/me/messages?access_token=${process.env.FB_PAGE_ACCESS_TOKEN}`,
    {
      recipient: { id: recipient },
      message: { text: message }
    }
  );
}

app.listen(3000, () => console.log('Serwer nasłuchuje na porcie 3000'));
```

#### 2.2. Konfiguracja funkcji specjalnych
- Implementacja Quick Replies (przyciski szybkiej odpowiedzi)
- Konfiguracja Persistent Menu (stałe menu)
- Implementacja obsługi załączników (zdjęcia, filmy)

#### 2.3. Mapowanie odpowiedzi Dialogflow na format Instagram
- Skonfiguruj formatowanie odpowiedzi tekstowych
- Dodaj obsługę przycisków i karuzeli
- Zaimplementuj obsługę załączników multimedialnych

### 3. Testowanie integracji Instagram

#### 3.1. Testy podstawowe
- Sprawdź rozpoznawanie prostych intencji
- Przetestuj odpowiedzi na standardowe pytania
- Sprawdź obsługę kontekstu rozmowy

#### 3.2. Testy zaawansowane
- Przetestuj obsługę złożonych scenariuszy konwersacji
- Sprawdź obsługę załączników i multimediów
- Przetestuj mechanizm przekazywania rozmowy do konsultanta

#### 3.3. Testy wydajnościowe
- Sprawdź czas odpowiedzi
- Przetestuj zachowanie przy wielu równoczesnych rozmowach
- Zweryfikuj limity API i potencjalne ograniczenia

## Integracja obu kanałów z monday.com

### 1. Konfiguracja monday.com

#### 1.1. Przygotowanie struktury danych
- Utwórz tablicę "Zapytania z chatbota"
- Skonfiguruj kolumny dla danych kontaktowych, treści zapytania, statusu, etc.
- Utwórz automatyzacje dla nowych zapytań

#### 1.2. Uzyskanie kluczy API
- Wygeneruj klucz API monday.com z odpowiednimi uprawnieniami
- Skonfiguruj webhooks dla powiadomień zwrotnych

### 2. Implementacja integracji z monday.com

#### 2.1. Tworzenie nowych elementów w monday.com
```javascript
// Przykładowa funkcja tworząca nowy element w monday.com
async function createMondayItem(customerName, phoneNumber, message, channel) {
  const axios = require('axios');
  
  const query = `mutation {
    create_item (
      board_id: ${process.env.MONDAY_BOARD_ID},
      group_id: "new_leads",
      item_name: "${customerName || 'Nowy klient'}",
      column_values: "{
        \\"text\\": \\"${message.replace(/"/g, '\\"')}\\",
        \\"phone\\": \\"${phoneNumber}\\",
        \\"status\\": {\\"label\\":\\"Nowe\\"},
        \\"source\\": {\\"label\\":\\"${channel}\\"}
      }"
    ) {
      id
    }
  }`;
  
  const response = await axios.post(
    'https://api.monday.com/v2',
    { query },
    {
      headers: {
        'Authorization': process.env.MONDAY_API_KEY,
        'Content-Type': 'application/json'
      }
    }
  );
  
  return response.data.data.create_item.id;
}
```

#### 2.2. Aktualizacja statusów i powiadomienia
- Implementacja mechanizmu aktualizacji statusu zapytań
- Konfiguracja powiadomień dla konsultantów
- Synchronizacja statusów między chatbotem a monday.com

## Wskazówki i najlepsze praktyki

### 1. Bezpieczeństwo
- Używaj zmiennych środowiskowych do przechowywania kluczy API i tokenów
- Implementuj walidację danych wejściowych
- Stosuj HTTPS dla wszystkich połączeń
- Regularnie rotuj klucze i tokeny dostępu

### 2. Wydajność
- Zaimplementuj mechanizm buforowania dla częstych zapytań
- Używaj asynchronicznych operacji dla zapytań do API
- Monitoruj czasy odpowiedzi i optymalizuj wąskie gardła

### 3. Obsługa błędów
- Implementuj szczegółowe logowanie błędów
- Przygotuj mechanizmy ponownych prób dla nieudanych żądań
- Skonfiguruj powiadomienia o krytycznych błędach

### 4. Monitorowanie
- Skonfiguruj narzędzia monitorowania (np. Google Cloud Monitoring)
- Ustaw alerty dla nietypowych wzorców użycia
- Regularnie analizuj logi i metryki wydajności

## Wymagane zasoby i dostępy

### 1. WhatsApp Business API
- Zweryfikowane konto WhatsApp Business
- Dostęp do API od wybranego dostawcy
- Zatwierdzone szablony wiadomości

### 2. Instagram/Facebook
- Konto Instagram Business
- Aplikacja Facebook Developer
- Tokeny dostępu do API Messenger Platform

### 3. Dialogflow
- Projekt Google Cloud Platform
- Skonfigurowany agent Dialogflow
- Klucze Service Account z odpowiednimi uprawnieniami

### 4. Infrastruktura
- Serwer dla middleware (np. Google Cloud Run, AWS Lambda)
- Baza danych dla przechowywania historii konwersacji (opcjonalnie)
- System monitorowania i logowania

### 5. monday.com
- Konto administratora monday.com
- Klucz API z uprawnieniami do tworzenia i aktualizacji elementów
- Skonfigurowane tablice i automatyzacje
