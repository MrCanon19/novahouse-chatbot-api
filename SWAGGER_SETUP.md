# 📚 Swagger UI Setup Guide

## Overview

Interaktywna dokumentacja API używająca **Swagger UI** z pełną specyfikacją **OpenAPI 3.0.3**.

## 🚀 Quick Start

### 1. Uruchom aplikację

```bash
# Lokalnie
python src/main.py

# Docker
make docker
```

### 2. Otwórz Swagger UI

Przejdź do: **http://localhost:5000/api-docs**

W produkcji: **https://glass-core-467907-e9.ey.r.appspot.com/api-docs**

## 📖 Struktura

### Pliki dokumentacji:

```
src/
├── docs/
│   ├── openapi.yaml     # OpenAPI 3.0.3 specification
│   └── swagger.yaml     # Stara wersja (deprecated)
└── routes/
    └── swagger_ui.py    # Swagger UI route
```

### Główne elementy OpenAPI spec:

- **Info**: Metadata, wersja, kontakt, licencja
- **Servers**: Production + localhost
- **Tags**: 7 kategorii endpointów
- **Security**: API Key authentication
- **Components**: Reusable schemas
- **Paths**: 8+ dokumentowanych endpointów

## 🔧 Konfiguracja

### 1. Dodaj route w `main.py`

```python
from src.routes.swagger_ui import swagger_ui_bp

# Register blueprint
app.register_blueprint(swagger_ui_bp)
```

### 2. Dostosuj OpenAPI spec

Edytuj `src/docs/openapi.yaml`:

```yaml
info:
  title: Your API Title
  version: 1.0.0
  description: Your description

servers:
  - url: https://your-domain.com
    description: Production
```

### 3. Dodaj nowy endpoint

```yaml
paths:
  /api/new-endpoint:
    get:
      tags:
        - Category
      summary: Short description
      operationId: operationName
      parameters:
        - name: param1
          in: query
          schema:
            type: string
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                type: object
```

## 📊 Features

### ✅ Zaimplementowane:

- **Swagger UI** - Interaktywny interfejs
- **OpenAPI 3.0.3** - Kompletna specyfikacja
- **8+ endpointów** - Dokumentowane API
- **Security schemas** - API Key auth
- **Request/Response examples** - Dla wszystkich endpointów
- **Try it out** - Testowanie w przeglądarce

### Dokumentowane endpointy:

1. `GET /api/health` - Health check
2. `POST /api/chatbot/message` - Chatbot conversation
3. `GET /api/knowledge/search` - Search knowledge base
4. `GET /api/leads` - List leads
5. `POST /api/leads` - Create lead
6. `GET /api/analytics/summary` - Analytics summary
7. `POST /api/backup/manual` - Manual backup
8. More...

## 🎨 Customization

### Zmiana wyglądu Swagger UI:

Edytuj `src/routes/swagger_ui.py`:

```html
<style>
  .swagger-ui .topbar {
    background-color: #your-color;
  }
  .swagger-ui .info .title {
    color: #your-color;
  }
</style>
```

### Konfiguracja UI:

```javascript
const ui = SwaggerUIBundle({
  // ... existing config
  defaultModelsExpandDepth: 2, // Model depth
  docExpansion: "full", // Expand all
  filter: true, // Enable filtering
  showExtensions: true, // Show x- extensions
});
```

## 🔒 Security

### API Key Authentication:

W Swagger UI kliknij **"Authorize"**:

```
Value: your-api-key-here
```

Lub dodaj w headerze:

```bash
curl -H "X-API-Key: your-key" https://api.example.com/endpoint
```

## 🧪 Testing

### Test w Swagger UI:

1. Kliknij endpoint
2. "Try it out"
3. Wypełnij parametry
4. "Execute"
5. Zobacz response

### Test curl:

```bash
# Health check
curl http://localhost:5000/api/health

# Chatbot message
curl -X POST http://localhost:5000/api/chatbot/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{"message": "Witam", "session_id": "test-123"}'

# Search knowledge
curl "http://localhost:5000/api/knowledge/search?query=projekt&limit=5" \
  -H "X-API-Key: your-key"
```

## 📝 Best Practices

### 1. **Pełna dokumentacja**

- Każdy endpoint musi mieć description
- Przykłady request/response
- Error responses (400, 401, 500)

### 2. **Reusable components**

```yaml
components:
  schemas:
    User:
      type: object
      properties:
        id: { type: integer }
        name: { type: string }

  # Reuse in paths:
  responses:
    "200":
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/User"
```

### 3. **Versioning**

```yaml
info:
  version: 2.3.1 # Zawsze aktualizuj!

servers:
  - url: https://api.example.com/v2
    description: API v2
```

### 4. **Tags dla organizacji**

```yaml
tags:
  - name: Users
    description: User management
  - name: Products
    description: Product catalog
```

### 5. **Security definitions**

```yaml
security:
  - ApiKeyAuth: []
  - OAuth2: [read, write]
```

## 🐛 Troubleshooting

### Problem: Swagger UI nie ładuje się

```bash
# Sprawdź czy route jest zarejestrowany
curl http://localhost:5000/api-docs

# Sprawdź czy openapi.yaml istnieje
ls -la src/docs/openapi.yaml
```

### Problem: CORS errors

Dodaj w `main.py`:

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"]
    }
})
```

### Problem: 404 na /api/openapi.yaml

Sprawdź ścieżkę w `swagger_ui.py`:

```python
docs_dir = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'docs'
)
```

## 🔗 Resources

- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)
- [OpenAPI Examples](https://github.com/OAI/OpenAPI-Specification/tree/main/examples)
- [Swagger Editor](https://editor.swagger.io/) - Online editor

## 🎯 Next Steps

1. ✅ Dodaj więcej endpointów do `openapi.yaml`
2. ✅ Dodaj przykłady dla każdego endpointu
3. ✅ Dodaj error responses
4. ✅ Stwórz Postman collection z OpenAPI
5. ✅ Dodaj do CI/CD: validation OpenAPI spec

## 📊 Monitoring

### Swagger usage analytics:

```javascript
// W swagger_ui.py dodaj tracking
window.onload = function () {
  const ui = SwaggerUIBundle({
    // ... config
    onComplete: function () {
      console.log("Swagger UI loaded");
      // Analytics tracking
    },
  });
};
```

---

**Happy Documenting! 📚**
