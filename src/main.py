import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
# KROK 1: Importujemy TYLKO obiekt 'db' z pliku, gdzie jest zdefiniowany.
from src.models.chatbot import db

# KROK 2: Tworzymy główną instancję aplikacji Flask.
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Włączenie CORS dla wszystkich endpointów.
CORS(app)

# KROK 3: Konfigurujemy i łączymy bazę danych z aplikacją.
# Od tego momentu 'db' wie o istnieniu 'app'.
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# KROK 4: DOPIERO TERAZ, gdy aplikacja i baza są połączone,
# importujemy trasy (blueprints), które z nich korzystają.
from src.routes.user import user_bp
from src.routes.chatbot import chatbot_bp
from src.routes.health import health_bp
from src.routes.analytics import analytics_bp
from src.routes.leads import leads_bp
from src.routes.intents import intents_bp
from src.routes.entities import entities_bp

# KROK 5: Rejestrujemy nasze trasy w aplikacji.
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
app.register_blueprint(health_bp, url_prefix='/api')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
app.register_blueprint(leads_bp, url_prefix='/api/leads')
app.register_blueprint(intents_bp, url_prefix='/api/intents')
app.register_blueprint(entities_bp, url_prefix='/api/entities')

# KROK 6: Tworzymy tabele w kontekście w pełni skonfigurowanej aplikacji.
with app.app_context():
    db.create_all()

# Reszta kodu do serwowania plików statycznych pozostaje bez zmian.
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
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Uruchomienie lokalne pozostaje bez zmian.
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
