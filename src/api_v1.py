"""
API v1 Blueprint
Versioned API endpoints for backward compatibility
"""
from flask import Blueprint

# Create v1 blueprint
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Import all route modules
from src.routes import (
    chatbot,
    analytics,
    leads,
    booking,
    knowledge,
    user,
    health,
    dashboard_widgets,
    qualification,
    search,
    file_upload,
    backup,
    ab_testing,
    entities,
    intents,
    i18n
)

# Register routes with v1 blueprint
def register_v1_routes(app):
    """Register all v1 routes with the Flask app"""
    
    # Chatbot routes
    api_v1.add_url_rule('/chat', 'chat', chatbot.chat, methods=['POST'])
    api_v1.add_url_rule('/chat/session/<session_id>', 'get_session', 
                        chatbot.get_session, methods=['GET'])
    
    # Analytics routes
    api_v1.add_url_rule('/analytics/events', 'analytics_events', 
                        analytics.get_events, methods=['GET'])
    api_v1.add_url_rule('/analytics/summary', 'analytics_summary', 
                        analytics.get_summary, methods=['GET'])
    
    # Lead management
    api_v1.add_url_rule('/leads', 'get_leads', leads.get_leads, methods=['GET'])
    api_v1.add_url_rule('/leads/<int:lead_id>', 'get_lead', 
                        leads.get_lead, methods=['GET'])
    api_v1.add_url_rule('/leads/<int:lead_id>', 'update_lead', 
                        leads.update_lead, methods=['PUT'])
    api_v1.add_url_rule('/leads/export', 'export_leads', 
                        leads.export_leads, methods=['GET'])
    
    # Booking/Appointments
    api_v1.add_url_rule('/appointments', 'get_appointments', 
                        booking.get_appointments, methods=['GET'])
    api_v1.add_url_rule('/appointments', 'create_appointment', 
                        booking.book_appointment, methods=['POST'])
    
    # Knowledge base
    api_v1.add_url_rule('/knowledge/portfolio', 'get_portfolio', 
                        knowledge.get_portfolio, methods=['GET'])
    api_v1.add_url_rule('/knowledge/process', 'get_process', 
                        knowledge.get_process, methods=['GET'])
    api_v1.add_url_rule('/knowledge/reviews', 'get_reviews', 
                        knowledge.get_reviews, methods=['GET'])
    
    # Health checks
    api_v1.add_url_rule('/health', 'health_check', 
                        health.health_check, methods=['GET'])
    
    # Dashboard widgets
    api_v1.add_url_rule('/dashboard/widgets', 'get_widgets', 
                        dashboard_widgets.get_widgets, methods=['GET'])
    
    # Search
    api_v1.add_url_rule('/search', 'search', search.search, methods=['GET'])
    
    # File uploads
    api_v1.add_url_rule('/upload', 'upload_file', 
                        file_upload.upload_file, methods=['POST'])
    
    # A/B Testing
    api_v1.add_url_rule('/ab-tests', 'get_ab_tests', 
                        ab_testing.get_tests, methods=['GET'])
    
    # Register blueprint with app
    app.register_blueprint(api_v1)
    
    return api_v1
