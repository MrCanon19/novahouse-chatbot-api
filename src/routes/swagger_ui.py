# type: ignore
"""
Swagger UI route for interactive API documentation
"""

import os

from flask import Blueprint, render_template_string, send_from_directory

swagger_ui_bp = Blueprint("swagger_ui", __name__)

SWAGGER_UI_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NovaHouse Chatbot API - Documentation</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.10.0/swagger-ui.css">
    <style>
        body {
            margin: 0;
            padding: 0;
        }
        .topbar {
            display: none;
        }
        .swagger-ui .info {
            margin: 20px 0;
        }
        .swagger-ui .info .title {
            font-size: 36px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>

    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.10.0/swagger-ui-bundle.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.10.0/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {
            const ui = SwaggerUIBundle({
                url: '/api/openapi.yaml',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout",
                defaultModelsExpandDepth: 1,
                defaultModelExpandDepth: 1,
                docExpansion: 'list',
                filter: true,
                showRequestHeaders: true,
                supportedSubmitMethods: ['get', 'post', 'put', 'delete', 'patch']
            });

            window.ui = ui;
        };
    </script>
</body>
</html>
"""


@swagger_ui_bp.route("/api-docs")
def swagger_ui():
    """Render Swagger UI"""
    return render_template_string(SWAGGER_UI_HTML)


@swagger_ui_bp.route("/api/openapi.yaml")
def openapi_spec():
    """Serve OpenAPI specification"""
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
    return send_from_directory(docs_dir, "openapi.yaml", mimetype="text/yaml")
