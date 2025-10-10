import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.chatbot import Intent, Entity, Conversation, Lead
from src.routes.chatbot import chatbot_bp
from src.routes.user import user_bp
from src.routes.health import health_bp
from src.monday_integration import create_monday_item, get_board_id_by_name, get_board_columns

app = Flask(__name__, static_folder=os.path.join(os_path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Włączenie CORS dla wszystkich endpointów
CORS(app)

# Ustawienie kluczy API jako zmiennych globalnych w aplikacji Flask
app.config['MONDAY_API_KEY'] = os.environ.get('MONDAY_API_KEY')
app.config['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
app.register_blueprint(health_bp, url_path='/health')

# Database config for Google Cloud SQL PostgreSQL
DB_USER = 'chatbot_user'
DB_PASSWORD = 'NovaHouse2024SecurePass'
DB_NAME = 'chatbot_db'
DB_CONNECTION_NAME = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

# Cloud SQL connection string for App Engine
if os.environ.get('GAE_ENV', '').startswith('standard'):
    # Running on App Engine
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host=/cloudsql/{DB_CONNECTION_NAME}'
else:
    # Running locally or in other environments
    DB_HOST = '35.205.83.191'  # Public IP of Cloud SQL instance
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(str(index_path)):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    # For local testing
    port = int(os.environ.get('PORT', 5000))
    debug = True # Set to True for local debugging
    app.run(host='0.0.0.0', port=port, debug=debug)


