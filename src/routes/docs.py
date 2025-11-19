"""
API Documentation Routes
========================
Swagger/OpenAPI documentation endpoints
"""

from flask import Blueprint, jsonify
import os
import yaml

docs_bp = Blueprint("docs", __name__)

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")


@docs_bp.route("/api/docs", methods=["GET"])
def api_docs():
    """Serve Swagger UI"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>NovaHouse Chatbot API Documentation</title>
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">  # noqa: E501
        <link rel="icon" type="image/png" href="https://novahouse.pl/favicon.ico">
        <style>
            html {
                box-sizing: border-box;
                overflow: -moz-scrollbars-vertical;
                overflow-y: scroll;
            }
            *, *:before, *:after {
                box-sizing: inherit;
            }
            body {
                margin: 0;
                padding: 0;
            }
            .topbar {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            }
            .swagger-ui .topbar .download-url-wrapper {
                display: none;
            }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>  # noqa: E501
        <script>
            window.onload = function() {
                const ui = SwaggerUIBundle({
                    url: "/api/docs/spec",
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "StandaloneLayout"
                });
                window.ui = ui;
            };
        </script>
    </body>
    </html>
    """


@docs_bp.route("/api/docs/spec", methods=["GET"])
def api_spec():
    """Serve OpenAPI specification"""
    try:
        spec_path = os.path.join(DOCS_DIR, "swagger.yaml")
        with open(spec_path, "r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
        return jsonify(spec)
    except Exception as e:
        return jsonify({"error": "Failed to load API specification", "details": str(e)}), 500


@docs_bp.route("/api/docs/redoc", methods=["GET"])
def redoc():
    """Serve ReDoc alternative documentation"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>NovaHouse Chatbot API - ReDoc</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">  # noqa: E501
        <style>
            body {
                margin: 0;
                padding: 0;
            }
        </style>
    </head>
    <body>
        <redoc spec-url='/api/docs/spec'></redoc>
        <script src="https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js"></script>  # noqa: E501
    </body>
    </html>
    """
