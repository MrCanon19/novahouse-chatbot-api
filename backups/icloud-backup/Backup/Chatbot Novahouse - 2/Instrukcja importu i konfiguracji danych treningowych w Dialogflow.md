# Instrukcja importu i konfiguracji danych treningowych w Dialogflow

## 1. Przygotowanie danych treningowych

### 1.1. Konwersja danych do formatu Dialogflow

#### Format intencji
Dialogflow wymaga danych w określonym formacie JSON. Poniżej przykładowy format dla intencji:

```json
{
  "id": "19556d13-5a75-4edc-9610-deadbeef1234",
  "name": "pakiety_waniliowy_info",
  "auto": true,
  "contexts": [],
  "responses": [
    {
      "resetContexts": false,
      "action": "pakiety.waniliowy",
      "affectedContexts": [],
      "parameters": [],
      "messages": [
        {
          "type": 0,
          "speech": "Pakiet Waniliowy to nasza podstawowa opcja wykończenia wnętrz, która kosztuje od 949 zł/m². Obejmuje malowanie ścian i sufitów, montaż drzwi wewnętrznych, położenie podłogi oraz kompleksowe wykończenie łazienki."
        }
      ],
      "defaultResponsePlatforms": {},
      "speech": []
    }
  ],
  "priority": 500000,
  "webhookUsed": false,
  "webhookForSlotFilling": false,
  "fallbackIntent": false,
  "events": [],
  "userSays": [
    {
      "id": "19556d13-5a75-4edc-9610-deadbeef5678",
      "data": [
        {
          "text": "Czym jest pakiet waniliowy",
          "userDefined": false
        }
      ],
      "isTemplate": false,
      "count": 0,
      "updated": 0
    },
    {
      "id": "19556d13-5a75-4edc-9610-deadbeef9012",
      "data": [
        {
          "text": "Ile kosztuje pakiet waniliowy",
          "userDefined": false
        }
      ],
      "isTemplate": false,
      "count": 0,
      "updated": 0
    }
  ],
  "followUpIntents": [],
  "liveAgentHandoff": false,
  "endInteraction": false,
  "conditionalResponses": [],
  "condition": "",
  "conditionalFollowupEvents": []
}
```

#### Format encji
Format JSON dla encji:

```json
{
  "id": "19556d13-5a75-4edc-9610-deadbeefabcd",
  "name": "pakiet_wykonczeniowy",
  "isOverridable": true,
  "isEnum": false,
  "isRegexp": false,
  "automatedExpansion": true,
  "allowFuzzyExtraction": true,
  "entries": [
    {
      "value": "waniliowy",
      "synonyms": [
        "waniliowy",
        "podstawowy",
        "najtańszy",
        "ekonomiczny",
        "standard"
      ]
    },
    {
      "value": "szafranowy",
      "synonyms": [
        "szafranowy",
        "komfortowy",
        "średni"
      ]
    },
    {
      "value": "pomarańczowy",
      "synonyms": [
        "pomarańczowy",
        "podwyższony",
        "wyższy standard"
      ]
    },
    {
      "value": "cynamonowy",
      "synonyms": [
        "cynamonowy",
        "premium",
        "luksusowy",
        "najdroższy"
      ]
    }
  ]
}
```

### 1.2. Skrypt konwersji danych z Markdown do formatu Dialogflow

Poniżej przykładowy skrypt Python do konwersji przygotowanych danych z formatu Markdown do formatu JSON Dialogflow:

```python
import re
import json
import uuid
import os

def generate_uuid():
    return str(uuid.uuid4())

def parse_intents_from_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Podział na sekcje intencji
    intent_sections = re.split(r'##\s+', content)[1:]  # Pomijamy nagłówek
    
    intents = []
    
    for section in intent_sections:
        lines = section.strip().split('\n')
        intent_name = lines[0].strip().lower().replace(' ', '_')
        
        # Zbieranie przykładowych wypowiedzi
        user_says = []
        examples_started = False
        
        for i, line in enumerate(lines):
            if line.startswith('### Przykładowe wypowiedzi:'):
                examples_started = True
                continue
            
            if examples_started and line.strip() and not line.startswith('#'):
                if line.startswith('- '):
                    user_says.append(line[2:].strip())
                else:
                    # Koniec sekcji przykładów
                    examples_started = False
        
        # Zbieranie odpowiedzi
        responses = []
        responses_started = False
        
        for i, line in enumerate(lines):
            if line.startswith('### Odpowiedzi:'):
                responses_started = True
                continue
            
            if responses_started and line.strip() and not line.startswith('#'):
                if line.startswith('- '):
                    responses.append(line[2:].strip())
                else:
                    # Koniec sekcji odpowiedzi
                    responses_started = False
        
        # Tworzenie obiektu intencji
        intent = {
            "id": generate_uuid(),
            "name": intent_name,
            "auto": True,
            "contexts": [],
            "responses": [
                {
                    "resetContexts": False,
                    "action": intent_name.replace('_', '.'),
                    "affectedContexts": [],
                    "parameters": [],
                    "messages": [
                        {
                            "type": 0,
                            "speech": responses[0] if responses else ""
                        }
                    ],
                    "defaultResponsePlatforms": {},
                    "speech": []
                }
            ],
            "priority": 500000,
            "webhookUsed": False,
            "webhookForSlotFilling": False,
            "fallbackIntent": False,
            "events": [],
            "userSays": [
                {
                    "id": generate_uuid(),
                    "data": [
                        {
                            "text": example,
                            "userDefined": False
                        }
                    ],
                    "isTemplate": False,
                    "count": 0,
                    "updated": 0
                } for example in user_says
            ],
            "followUpIntents": [],
            "liveAgentHandoff": False,
            "endInteraction": False,
            "conditionalResponses": [],
            "condition": "",
            "conditionalFollowupEvents": []
        }
        
        intents.append(intent)
    
    return intents

def parse_entities_from_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Podział na sekcje encji
    entity_sections = re.split(r'##\s+', content)[1:]  # Pomijamy nagłówek
    
    entities = []
    
    for section in entity_sections:
        lines = section.strip().split('\n')
        entity_name = lines[0].strip().lower().replace(' ', '_')
        
        # Zbieranie wartości i synonimów
        entries = []
        entry_started = False
        current_value = None
        current_synonyms = []
        
        for i, line in enumerate(lines):
            if line.startswith('### Wartości:'):
                entry_started = True
                continue
            
            if entry_started and line.strip() and not line.startswith('#'):
                if line.startswith('- '):
                    # Jeśli mamy już wartość, dodajemy poprzednią encję
                    if current_value:
                        entries.append({
                            "value": current_value,
                            "synonyms": [current_value] + current_synonyms
                        })
                    
                    # Rozpoczynamy nową encję
                    parts = line[2:].strip().split(':')
                    current_value = parts[0].strip()
                    current_synonyms = []
                    
                    # Jeśli są synonimy w tej samej linii
                    if len(parts) > 1 and parts[1].strip():
                        synonyms = parts[1].strip().split(',')
                        current_synonyms = [s.strip() for s in synonyms]
                elif line.startswith('  - ') and current_value:
                    # Dodajemy synonim do bieżącej wartości
                    current_synonyms.append(line[4:].strip())
                else:
                    # Koniec sekcji wartości
                    entry_started = False
        
        # Dodajemy ostatnią encję
        if current_value:
            entries.append({
                "value": current_value,
                "synonyms": [current_value] + current_synonyms
            })
        
        # Tworzenie obiektu encji
        entity = {
            "id": generate_uuid(),
            "name": entity_name,
            "isOverridable": True,
            "isEnum": False,
            "isRegexp": False,
            "automatedExpansion": True,
            "allowFuzzyExtraction": True,
            "entries": entries
        }
        
        entities.append(entity)
    
    return entities

def main():
    # Ścieżki do plików Markdown
    intents_md_path = '/home/ubuntu/chatbot_data/nlu/intencje.md'
    entities_md_path = '/home/ubuntu/chatbot_data/nlu/encje.md'
    
    # Ścieżki do plików wyjściowych JSON
    output_dir = '/home/ubuntu/chatbot_data/dialogflow_import'
    os.makedirs(output_dir, exist_ok=True)
    
    # Konwersja intencji
    intents = parse_intents_from_markdown(intents_md_path)
    
    # Zapisywanie każdej intencji do osobnego pliku
    for intent in intents:
        intent_file_path = os.path.join(output_dir, f"{intent['name']}.json")
        with open(intent_file_path, 'w', encoding='utf-8') as file:
            json.dump(intent, file, ensure_ascii=False, indent=2)
    
    # Konwersja encji
    entities = parse_entities_from_markdown(entities_md_path)
    
    # Zapisywanie każdej encji do osobnego pliku
    for entity in entities:
        entity_file_path = os.path.join(output_dir, f"{entity['name']}.json")
        with open(entity_file_path, 'w', encoding='utf-8') as file:
            json.dump(entity, file, ensure_ascii=False, indent=2)
    
    print(f"Wygenerowano {len(intents)} plików intencji i {len(entities)} plików encji w katalogu {output_dir}")

if __name__ == "__main__":
    main()
```

### 1.3. Przygotowanie plików ZIP do importu

Dialogflow wymaga, aby pliki intencji i encji były spakowane w odpowiedniej strukturze:

```
agent.zip
├── intents/
│   ├── pakiety_waniliowy_info.json
│   ├── pakiety_szafranowy_info.json
│   └── ...
├── entities/
│   ├── pakiet_wykonczeniowy.json
│   ├── metraz_lokalu.json
│   └── ...
└── agent.json
```

Plik `agent.json` powinien zawierać podstawowe informacje o agencie:

```json
{
  "description": "Chatbot NovaHouse do obsługi klientów zainteresowanych wykańczaniem wnętrz pod klucz",
  "language": "pl",
  "shortDescription": "Chatbot NovaHouse",
  "examples": "",
  "linkToDocs": "",
  "displayName": "NovaHouse Chatbot",
  "disableInteractionLogs": false,
  "disableStackdriverLogs": false,
  "defaultTimezone": "Europe/Warsaw",
  "webhook": {
    "url": "",
    "username": "",
    "headers": {},
    "available": false,
    "useForDomains": false,
    "cloudFunctionsEnabled": false,
    "cloudFunctionsInitialized": false
  },
  "isPrivate": true,
  "mlMinConfidence": 0.3,
  "supportedLanguages": [],
  "enableOnePlatformApi": true
}
```

Skrypt do przygotowania pliku ZIP:

```python
import os
import json
import shutil
import zipfile

def prepare_agent_zip(input_dir, output_zip):
    # Tworzenie tymczasowej struktury katalogów
    temp_dir = '/tmp/dialogflow_agent'
    intents_dir = os.path.join(temp_dir, 'intents')
    entities_dir = os.path.join(temp_dir, 'entities')
    
    # Usuwanie istniejącego katalogu tymczasowego
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    # Tworzenie katalogów
    os.makedirs(intents_dir, exist_ok=True)
    os.makedirs(entities_dir, exist_ok=True)
    
    # Kopiowanie plików intencji
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            with open(os.path.join(input_dir, file_name), 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                if 'userSays' in data:  # To jest intencja
                    shutil.copy(
                        os.path.join(input_dir, file_name),
                        os.path.join(intents_dir, file_name)
                    )
                elif 'entries' in data:  # To jest encja
                    shutil.copy(
                        os.path.join(input_dir, file_name),
                        os.path.join(entities_dir, file_name)
                    )
    
    # Tworzenie pliku agent.json
    agent_config = {
        "description": "Chatbot NovaHouse do obsługi klientów zainteresowanych wykańczaniem wnętrz pod klucz",
        "language": "pl",
        "shortDescription": "Chatbot NovaHouse",
        "examples": "",
        "linkToDocs": "",
        "displayName": "NovaHouse Chatbot",
        "disableInteractionLogs": false,
        "disableStackdriverLogs": false,
        "defaultTimezone": "Europe/Warsaw",
        "webhook": {
            "url": "",
            "username": "",
            "headers": {},
            "available": false,
            "useForDomains": false,
            "cloudFunctionsEnabled": false,
            "cloudFunctionsInitialized": false
        },
        "isPrivate": true,
        "mlMinConfidence": 0.3,
        "supportedLanguages": [],
        "enableOnePlatformApi": true
    }
    
    with open(os.path.join(temp_dir, 'agent.json'), 'w', encoding='utf-8') as file:
        json.dump(agent_config, file, ensure_ascii=False, indent=2)
    
    # Tworzenie pliku ZIP
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    print(f"Plik ZIP agenta został utworzony: {output_zip}")

if __name__ == "__main__":
    input_dir = '/home/ubuntu/chatbot_data/dialogflow_import'
    output_zip = '/home/ubuntu/chatbot_data/novahouse_agent.zip'
    prepare_agent_zip(input_dir, output_zip)
```

## 2. Import danych do Dialogflow

### 2.1. Import przez konsolę Dialogflow

#### Krok 1: Logowanie do konsoli Dialogflow
1. Przejdź do [konsoli Dialogflow](https://dialogflow.cloud.google.com/)
2. Zaloguj się na konto Google
3. Wybierz projekt Google Cloud Platform

#### Krok 2: Tworzenie nowego agenta
1. Kliknij przycisk "Create Agent" (lub "Utwórz agenta")
2. Wprowadź nazwę agenta (np. "NovaHouse Chatbot")
3. Wybierz język domyślny (polski)
4. Wybierz strefę czasową (Europe/Warsaw)
5. Wybierz projekt Google Cloud Platform
6. Kliknij "Create" (lub "Utwórz")

#### Krok 3: Import agenta z pliku ZIP
1. Kliknij ikonę ustawień obok nazwy agenta
2. Wybierz zakładkę "Export and Import" (lub "Eksport i import")
3. Kliknij "Import from ZIP" (lub "Importuj z ZIP")
4. Wybierz przygotowany plik ZIP
5. Kliknij "Import" (lub "Importuj")
6. Poczekaj na zakończenie importu

### 2.2. Import przez API Dialogflow

Alternatywnie, można zaimportować dane przez API Dialogflow. Poniżej przykładowy skrypt Python:

```python
import os
import json
from google.cloud import dialogflow_v2 as dialogflow
from google.protobuf.json_format import MessageToDict, ParseDict

def import_intents(project_id, intents_dir):
    """Importuje intencje z plików JSON do agenta Dialogflow."""
    client = dialogflow.IntentsClient()
    parent = client.agent_path(project_id)
    
    for file_name in os.listdir(intents_dir):
        if not file_name.endswith('.json'):
            continue
        
        file_path = os.path.join(intents_dir, file_name)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            intent_json = json.load(file)
        
        # Usuwanie pól, które nie są obsługiwane przez API
        if 'id' in intent_json:
            del intent_json['id']
        
        for user_say in intent_json.get('userSays', []):
            if 'id' in user_say:
                del user_say['id']
        
        # Konwersja JSON do obiektu Intent
        intent = ParseDict(intent_json, dialogflow.Intent())
        
        # Tworzenie intencji
        response = client.create_intent(parent=parent, intent=intent)
        print(f"Utworzono intencję: {response.display_name}")

def import_entities(project_id, entities_dir):
    """Importuje encje z plików JSON do agenta Dialogflow."""
    client = dialogflow.EntityTypesClient()
    parent = client.agent_path(project_id)
    
    for file_name in os.listdir(entities_dir):
        if not file_name.endswith('.json'):
            continue
        
        file_path = os.path.join(entities_dir, file_name)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            entity_json = json.load(file)
        
        # Usuwanie pól, które nie są obsługiwane przez API
        if 'id' in entity_json:
            del entity_json['id']
        
        # Konwersja JSON do obiektu EntityType
        entity_type = ParseDict(entity_json, dialogflow.EntityType())
        
        # Tworzenie encji
        response = client.create_entity_type(parent=parent, entity_type=entity_type)
        print(f"Utworzono encję: {response.display_name}")

def main():
    # Konfiguracja
    project_id = 'novahouse-chatbot'  # ID projektu Google Cloud Platform
    intents_dir = '/home/ubuntu/chatbot_data/dialogflow_import/intents'
    entities_dir = '/home/ubuntu/chatbot_data/dialogflow_import/entities'
    
    # Import intencji i encji
    import_intents(project_id, intents_dir)
    import_entities(project_id, entities_dir)

if __name__ == "__main__":
    main()
```

## 3. Konfiguracja i optymalizacja danych treningowych

### 3.1. Weryfikacja importu

Po zaimportowaniu danych należy sprawdzić, czy wszystkie intencje i encje zostały poprawnie zaimportowane:

1. Przejdź do sekcji "Intents" (lub "Intencje") w konsoli Dialogflow
2. Sprawdź, czy wszystkie intencje są widoczne i mają poprawne przykłady wypowiedzi
3. Przejdź do sekcji "Entities" (lub "Encje")
4. Sprawdź, czy wszystkie encje są widoczne i mają poprawne wartości i synonimy

### 3.2. Konfiguracja kontekstów

Konteksty w Dialogflow pozwalają na kontrolowanie przepływu konwersacji. Poniżej przykład konfiguracji kontekstów:

1. Przejdź do intencji, która powinna używać kontekstu (np. "pakiety_szczegoly")
2. W sekcji "Contexts" (lub "Konteksty") dodaj kontekst wejściowy (np. "pakiet_wybrany")
3. Przejdź do intencji, która powinna ustawiać kontekst (np. "wybor_pakietu")
4. W sekcji "Responses" (lub "Odpowiedzi") dodaj kontekst wyjściowy (np. "pakiet_wybrany")
5. Ustaw czas życia kontekstu (np. 5)

### 3.3. Konfiguracja parametrów

Parametry pozwalają na wyodrębnienie informacji z wypowiedzi użytkownika:

1. Przejdź do intencji, która powinna wyodrębniać parametry (np. "wybor_pakietu")
2. W sekcji "Action and parameters" (lub "Akcja i parametry") dodaj nowy parametr
3. Ustaw nazwę parametra (np. "pakiet")
4. Wybierz encję (np. "@pakiet_wykonczeniowy")
5. Zaznacz opcję "Required" (lub "Wymagany"), jeśli parametr jest obowiązkowy
6. Dodaj pytanie o brakujący parametr (np. "Który pakiet Cię interesuje: waniliowy, szafranowy, pomarańczowy czy cynamonowy?")

### 3.4. Konfiguracja odpowiedzi

Odpowiedzi można dostosować do wyodrębnionych parametrów:

1. Przejdź do intencji, która powinna używać parametrów w odpowiedzi
2. W sekcji "Responses" (lub "Odpowiedzi") edytuj odpowiedź tekstową
3. Użyj parametrów w tekście odpowiedzi (np. "Wybrałeś pakiet $pakiet. Oto szczegóły:")
4. Dodaj warianty odpowiedzi, aby chatbot nie powtarzał się

### 3.5. Konfiguracja zdarzeń

Zdarzenia pozwalają na wyzwalanie intencji bez wypowiedzi użytkownika:

1. Przejdź do intencji, która powinna być wyzwalana przez zdarzenie (np. "powitanie")
2. W sekcji "Events" (lub "Zdarzenia") dodaj nowe zdarzenie
3. Wprowadź nazwę zdarzenia (np. "WELCOME")

### 3.6. Trenowanie modelu

Po zakończeniu konfiguracji należy wytrenować model:

1. Kliknij przycisk "Train" (lub "Trenuj") w górnej części konsoli Dialogflow
2. Poczekaj na zakończenie trenowania
3. Przetestuj agenta w panelu testowym po prawej stronie

## 4. Testowanie i optymalizacja

### 4.1. Testowanie rozpoznawania intencji

1. W panelu testowym wprowadź przykładowe wypowiedzi użytkownika
2. Sprawdź, czy agent poprawnie rozpoznaje intencje
3. Zwróć uwagę na pewność rozpoznania (confidence)
4. Jeśli pewność jest niska lub intencja jest rozpoznawana niepoprawnie, dodaj więcej przykładów wypowiedzi

### 4.2. Testowanie wyodrębniania parametrów

1. W panelu testowym wprowadź wypowiedzi zawierające parametry
2. Sprawdź, czy agent poprawnie wyodrębnia parametry
3. Przetestuj różne warianty wypowiedzi (np. różne synonimy)
4. Jeśli parametry nie są poprawnie wyodrębniane, dodaj więcej przykładów lub zaktualizuj encje

### 4.3. Testowanie przepływów konwersacji

1. Przeprowadź pełne scenariusze konwersacji
2. Sprawdź, czy konteksty działają poprawnie
3. Przetestuj różne ścieżki konwersacji
4. Zwróć uwagę na płynność przejść między intencjami

### 4.4. Optymalizacja na podstawie wyników testów

1. Dodaj więcej przykładów wypowiedzi dla intencji, które są słabo rozpoznawane
2. Zaktualizuj encje o dodatkowe synonimy
3. Dostosuj konteksty, aby poprawić przepływ konwersacji
4. Zaktualizuj odpowiedzi, aby były bardziej naturalne i pomocne

## 5. Integracja z fulfillment

### 5.1. Konfiguracja fulfillment

Fulfillment pozwala na dynamiczne generowanie odpowiedzi:

1. Przejdź do sekcji "Fulfillment" (lub "Realizacja") w konsoli Dialogflow
2. Włącz opcję "Webhook"
3. Wprowadź URL webhooków (np. adres serwera middleware)
4. Skonfiguruj nagłówki (np. klucz autoryzacyjny)
5. Zapisz konfigurację

### 5.2. Implementacja webhooków

Przykładowy kod serwera webhooków w Node.js:

```javascript
const express = require('express');
const bodyParser = require('body-parser');
const app = express();

app.use(bodyParser.json());

app.post('/webhook', (req, res) => {
  const intent = req.body.queryResult.intent.displayName;
  const parameters = req.body.queryResult.parameters;
  
  let fulfillmentText = '';
  
  switch (intent) {
    case 'pakiety_waniliowy_info':
      fulfillmentText = `Pakiet Waniliowy to nasza podstawowa opcja wykończenia wnętrz, która kosztuje od 949 zł/m². Obejmuje malowanie ścian i sufitów, montaż drzwi wewnętrznych, położenie podłogi oraz kompleksowe wykończenie łazienki.`;
      break;
    
    case 'wybor_pakietu':
      const pakiet = parameters.pakiet || 'waniliowy';
      
      switch (pakiet) {
        case 'waniliowy':
          fulfillmentText = `Wybrałeś pakiet Waniliowy. To nasza podstawowa opcja w cenie od 949 zł/m². Czy chcesz poznać szczegóły tego pakietu?`;
          break;
        case 'szafranowy':
          fulfillmentText = `Wybrałeś pakiet Szafranowy. To nasza komfortowa opcja w cenie od 1099 zł/m². Czy chcesz poznać szczegóły tego pakietu?`;
          break;
        case 'pomarańczowy':
          fulfillmentText = `Wybrałeś pakiet Pomarańczowy. To nasza podwyższona opcja w cenie od 1399 zł/m². Czy chcesz poznać szczegóły tego pakietu?`;
          break;
        case 'cynamonowy':
          fulfillmentText = `Wybrałeś pakiet Cynamonowy. To nasza premium opcja w cenie od 1999 zł/m². Czy chcesz poznać szczegóły tego pakietu?`;
          break;
        default:
          fulfillmentText = `Nie rozpoznałem wybranego pakietu. Oferujemy pakiety: Waniliowy, Szafranowy, Pomarańczowy i Cynamonowy. Który Cię interesuje?`;
      }
      break;
    
    default:
      fulfillmentText = `Przepraszam, nie mogę obsłużyć tej intencji.`;
  }
  
  res.json({
    fulfillmentText: fulfillmentText
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Serwer nasłuchuje na porcie ${PORT}`);
});
```

### 5.3. Włączenie fulfillment dla intencji

1. Przejdź do intencji, która powinna używać fulfillment
2. W sekcji "Fulfillment" (lub "Realizacja") włącz opcję "Enable webhook call for this intent" (lub "Włącz wywołanie webhooków dla tej intencji")
3. Zapisz intencję

## 6. Eksport i backup danych

### 6.1. Eksport agenta

Regularne tworzenie kopii zapasowych jest ważne:

1. Kliknij ikonę ustawień obok nazwy agenta
2. Wybierz zakładkę "Export and Import" (lub "Eksport i import")
3. Kliknij "Export as ZIP" (lub "Eksportuj jako ZIP")
4. Zapisz plik ZIP w bezpiecznym miejscu

### 6.2. Eksport przez API

Można również eksportować agenta przez API:

```python
from google.cloud import dialogflow_v2 as dialogflow
import os

def export_agent(project_id, output_file):
    """Eksportuje agenta Dialogflow do pliku ZIP."""
    client = dialogflow.AgentsClient()
    parent = client.agent_path(project_id)
    
    response = client.export_agent(parent=parent)
    
    with open(output_file, 'wb') as file:
        file.write(response.agent_content)
    
    print(f"Agent został wyeksportowany do pliku: {output_file}")

if __name__ == "__main__":
    project_id = 'novahouse-chatbot'  # ID projektu Google Cloud Platform
    output_file = '/home/ubuntu/chatbot_data/novahouse_agent_backup.zip'
    export_agent(project_id, output_file)
```

## 7. Najlepsze praktyki

### 7.1. Organizacja intencji

- Używaj spójnej konwencji nazewnictwa (np. `kategoria_akcja_szczegoly`)
- Grupuj powiązane intencje (np. używając prefiksów)
- Unikaj zbyt ogólnych intencji, które mogą kolidować z innymi

### 7.2. Optymalizacja przykładów wypowiedzi

- Dodaj co najmniej 10-15 przykładów dla każdej intencji
- Używaj różnych sformułowań i struktur zdań
- Uwzględnij typowe błędy pisowni i interpunkcji
- Unikaj przykładów, które mogą pasować do wielu intencji

### 7.3. Efektywne wykorzystanie kontekstów

- Używaj kontekstów do kontrolowania przepływu konwersacji
- Ustaw odpowiedni czas życia kontekstów (zwykle 5-10)
- Używaj hierarchii kontekstów dla złożonych scenariuszy
- Regularnie testuj przepływy konwersacji z kontekstami

### 7.4. Monitorowanie i aktualizacja

- Regularnie analizuj logi konwersacji
- Identyfikuj nierozpoznane intencje i dodawaj nowe przykłady
- Aktualizuj bazę wiedzy na podstawie nowych pytań
- Testuj chatbota z rzeczywistymi użytkownikami i zbieraj feedback

## 8. Rozwiązywanie problemów

### 8.1. Niska pewność rozpoznawania intencji

- Dodaj więcej zróżnicowanych przykładów wypowiedzi
- Sprawdź, czy nie ma konfliktu między podobnymi intencjami
- Zwiększ minimalny próg pewności w ustawieniach agenta
- Rozważ użycie encji do lepszego rozróżniania intencji

### 8.2. Problemy z kontekstami

- Sprawdź, czy konteksty są poprawnie ustawione
- Zweryfikuj czas życia kontekstów
- Użyj narzędzia do debugowania kontekstów w konsoli Dialogflow
- Przetestuj pełne scenariusze konwersacji

### 8.3. Problemy z parametrami

- Sprawdź, czy encje są poprawnie zdefiniowane
- Dodaj więcej synonimów do encji
- Użyj systemu wyodrębniania parametrów w panelu testowym
- Sprawdź, czy parametry są poprawnie używane w odpowiedziach

### 8.4. Problemy z webhookami

- Sprawdź, czy URL webhooków jest poprawny i dostępny
- Zweryfikuj format odpowiedzi z webhooków
- Sprawdź logi serwera webhooków
- Użyj narzędzi do debugowania webhooków (np. ngrok)

## 9. Zaawansowane funkcje

### 9.1. Integracja z Knowledge Base

Dialogflow oferuje funkcję Knowledge Base, która pozwala na automatyczne generowanie odpowiedzi na podstawie dokumentów:

1. Przejdź do sekcji "Knowledge" (lub "Wiedza") w konsoli Dialogflow
2. Kliknij "Create Knowledge Base" (lub "Utwórz bazę wiedzy")
3. Wprowadź nazwę bazy wiedzy (np. "NovaHouse FAQ")
4. Kliknij "Create" (lub "Utwórz")
5. Dodaj dokumenty (np. pliki FAQ, dokumenty PDF, strony internetowe)
6. Skonfiguruj odpowiedzi generowane na podstawie bazy wiedzy

### 9.2. Integracja z LUIS (Language Understanding)

Dla bardziej zaawansowanego rozpoznawania języka naturalnego można zintegrować Dialogflow z LUIS:

1. Utwórz aplikację LUIS w [portalu LUIS](https://www.luis.ai/)
2. Skonfiguruj intencje i encje w LUIS
3. Wytrenuj model LUIS
4. Zintegruj LUIS z webhookami Dialogflow
5. Użyj wyników LUIS do poprawy rozpoznawania intencji

### 9.3. Analiza sentymentu

Dialogflow może analizować sentyment wypowiedzi użytkownika:

1. Włącz analizę sentymentu w ustawieniach agenta
2. Użyj wyników analizy sentymentu w webhookach
3. Dostosuj odpowiedzi na podstawie sentymentu (np. bardziej empatyczne odpowiedzi dla negatywnego sentymentu)

### 9.4. Integracja z systemami CRM

Można zintegrować Dialogflow z systemami CRM, takimi jak monday.com:

1. Skonfiguruj webhooks do komunikacji z API CRM
2. Implementuj funkcje do tworzenia i aktualizacji rekordów CRM
3. Użyj danych z CRM do personalizacji odpowiedzi
4. Synchronizuj historię konwersacji z CRM

## 10. Podsumowanie

Proces importu i konfiguracji danych treningowych w Dialogflow obejmuje:

1. Przygotowanie danych w odpowiednim formacie
2. Import danych do Dialogflow
3. Konfigurację i optymalizację intencji, encji, kontekstów i parametrów
4. Testowanie i optymalizację na podstawie wyników testów
5. Integrację z fulfillment dla dynamicznych odpowiedzi
6. Regularne tworzenie kopii zapasowych
7. Stosowanie najlepszych praktyk i rozwiązywanie problemów

Prawidłowo skonfigurowany agent Dialogflow z wysokiej jakości danymi treningowymi jest kluczem do sukcesu chatbota NovaHouse.
