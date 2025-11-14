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

# Initialize WebSocket support (v2.3)
from src.services.websocket_service import socketio
socketio.init_app(app)

# KROK 3: Konfigurujemy i łączymy bazę danych z aplikacją.
# Od tego momentu 'db' wie o istnieniu 'app'.
db_url = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}")
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
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
from src.routes.qualification import qualification_bp
from src.routes.booking import booking_bp
from src.routes.knowledge import knowledge_bp
from src.routes.docs import docs_bp
from src.routes.ab_testing import ab_testing_bp
from src.routes.i18n import i18n_bp
# New v2.3 routes
from src.routes.dashboard_widgets import dashboard_widgets
from src.routes.backup import backup_routes
from src.routes.search import search_routes
from src.routes.file_upload import file_upload_routes

# KROK 5: Rejestrujemy nasze trasy w aplikacji.
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
app.register_blueprint(health_bp, url_prefix='/api')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
app.register_blueprint(leads_bp, url_prefix='/api/leads')
app.register_blueprint(intents_bp, url_prefix='/api/intents')
app.register_blueprint(entities_bp, url_prefix='/api/entities')
app.register_blueprint(qualification_bp, url_prefix='/api/qualification')
app.register_blueprint(booking_bp, url_prefix='/api/booking')
app.register_blueprint(knowledge_bp, url_prefix='/api/knowledge')
app.register_blueprint(docs_bp)
app.register_blueprint(ab_testing_bp, url_prefix='/api/ab-testing')
app.register_blueprint(i18n_bp, url_prefix='/api/i18n')
# Register v2.3 routes
app.register_blueprint(dashboard_widgets)
app.register_blueprint(backup_routes)
app.register_blueprint(search_routes)
app.register_blueprint(file_upload_routes)

# KROK 6: Tworzymy tabele w kontekście w pełni skonfigurowanej aplikacji.
with app.app_context():
    db.create_all()
    
    # Initialize v2.3 services
    try:
        from src.services.redis_service import warm_redis_cache
        warm_redis_cache()
        print("✅ Redis cache warmed")
    except Exception as e:
        print(f"⚠️  Redis cache warming skipped: {e}")
    
    try:
        from src.services.search_service import search_service
        search_service.index_knowledge_base()
        print("✅ Search index built")
    except Exception as e:
        print(f"⚠️  Search indexing skipped: {e}")
    
    try:
        from src.services.backup_service import backup_service
        backup_service.schedule_automated_backup()
        print("✅ Automated backup scheduled")
    except Exception as e:
        print(f"⚠️  Backup scheduling skipped: {e}")

# Reszta kodu do serwowania plików statycznych pozostaje bez zmian.
@app.route('/admin')

@app.route("/qualification")
def qualification_page():
    return app.send_static_file("qualification.html")
def admin_dashboard():
    return app.send_static_file('admin-dashboard.html')

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
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_ENV') != 'production'
    # Use socketio.run instead of app.run for WebSocket support
    socketio.run(app, host='0.0.0.0', port=port, debug=debug)
