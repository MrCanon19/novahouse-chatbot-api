#!/bin/bash
# Generate API client SDKs from OpenAPI specification

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OPENAPI_SPEC="$PROJECT_ROOT/src/docs/openapi.yaml"
OUTPUT_DIR="$PROJECT_ROOT/clients"

echo "🚀 Generating API Client SDKs..."

# Check if openapi-generator-cli is installed
if ! command -v openapi-generator-cli &> /dev/null; then
    echo "❌ openapi-generator-cli not found!"
    echo "Install with: npm install -g @openapitools/openapi-generator-cli"
    echo "Or use Docker: docker pull openapitools/openapi-generator-cli"
    exit 1
fi

# Check if OpenAPI spec exists
if [ ! -f "$OPENAPI_SPEC" ]; then
    echo "❌ OpenAPI spec not found: $OPENAPI_SPEC"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "📝 OpenAPI Spec: $OPENAPI_SPEC"
echo "📦 Output Directory: $OUTPUT_DIR"
echo ""

# Generate Python client
echo "🐍 Generating Python client..."
openapi-generator-cli generate \
    -i "$OPENAPI_SPEC" \
    -g python \
    -o "$OUTPUT_DIR/python" \
    --additional-properties=packageName=novahouse_client,projectName=novahouse-chatbot-client,packageVersion=2.3.1

echo "✅ Python client generated: $OUTPUT_DIR/python"

# Generate JavaScript/TypeScript client
echo "📦 Generating JavaScript/TypeScript client..."
openapi-generator-cli generate \
    -i "$OPENAPI_SPEC" \
    -g typescript-axios \
    -o "$OUTPUT_DIR/typescript" \
    --additional-properties=npmName=@novahouse/chatbot-client,npmVersion=2.3.1,supportsES6=true

echo "✅ TypeScript client generated: $OUTPUT_DIR/typescript"

# Generate documentation
echo "📚 Generating API documentation..."
openapi-generator-cli generate \
    -i "$OPENAPI_SPEC" \
    -g html2 \
    -o "$OUTPUT_DIR/docs"

echo "✅ Documentation generated: $OUTPUT_DIR/docs"

# Create README for clients
cat > "$OUTPUT_DIR/README.md" << 'EOF'
# NovaHouse Chatbot API Clients

Auto-generated API clients from OpenAPI specification.

## Python Client

```bash
cd python
pip install -e .
```

**Usage:**
```python
from novahouse_client import ApiClient, Configuration
from novahouse_client.api import ChatbotApi

# Configure client
config = Configuration(
    host="https://glass-core-467907-e9.ey.r.appspot.com"
)

# Create API client
with ApiClient(config) as api_client:
    chatbot_api = ChatbotApi(api_client)
    
    # Send chat message
    response = chatbot_api.chat_post({
        "message": "Tell me about NovaHouse packages",
        "session_id": "test-session"
    })
    
    print(response)
```

## TypeScript Client

```bash
cd typescript
npm install
```

**Usage:**
```typescript
import { ChatbotApi, Configuration } from '@novahouse/chatbot-client';

const config = new Configuration({
    basePath: 'https://glass-core-467907-e9.ey.r.appspot.com'
});

const api = new ChatbotApi(config);

const response = await api.chatPost({
    message: 'Tell me about NovaHouse packages',
    session_id: 'test-session'
});

console.log(response.data);
```

## Documentation

Open `docs/index.html` in your browser for full API documentation.

## Regenerating Clients

To regenerate clients after API changes:

```bash
./scripts/generate_clients.sh
```

## Requirements

- OpenAPI Generator CLI: `npm install -g @openapitools/openapi-generator-cli`
- Or use Docker: `docker pull openapitools/openapi-generator-cli`
EOF

echo ""
echo "✨ All clients generated successfully!"
echo ""
echo "📚 Next steps:"
echo "  1. Python: cd $OUTPUT_DIR/python && pip install -e ."
echo "  2. TypeScript: cd $OUTPUT_DIR/typescript && npm install"
echo "  3. Docs: open $OUTPUT_DIR/docs/index.html"
