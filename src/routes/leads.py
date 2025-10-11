"""
Lead management endpoints
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.chatbot import db, Lead, Conversation
from src.models.analytics import UserEngagement

leads_bp = Blueprint('leads', __name__)

@leads_bp.route('/', methods=['POST'])
def create_lead():
    """Utwórz nowy lead z rozmowy"""
    try:
        data = request.get_json()
        
        # Walidacja wymaganych pól
        required_fields = ['name']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: name'
            }), 400
        
        # Utwórz lead
        lead = Lead(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            message=data.get('message', ''),
            source=data.get('source', 'chatbot'),
            status='new',
            session_id=data.get('session_id'),
            interested_package=data.get('interested_package'),
            property_size=data.get('property_size'),
            property_type=data.get('property_type'),
            location=data.get('location'),
            additional_info=data.get('additional_info')
        )
        db.session.add(lead)
        
        # Track engagement if session_id provided
        if data.get('session_id'):
            try:
                engagement = UserEngagement(
                    session_id=data['session_id'],
                    conversion_event='lead_created'
                )
                db.session.add(engagement)
            except Exception as e:
                print(f"Engagement tracking error: {e}")
        
        db.session.commit()
        
        # Monday.com integration will be added here
        try:
            from src.integrations.monday_client import MondayClient
            monday = MondayClient()
            monday_item_id = monday.create_lead_item({
                'name': lead.name,
                'email': lead.email or '',
                'phone': lead.phone or '',
                'message': lead.message or ''
            })
            if monday_item_id:
                lead.monday_item_id = monday_item_id
                db.session.commit()
        except Exception as e:
            print(f"Monday.com integration error: {e}")
            # Don't fail lead creation if Monday integration fails
        
        return jsonify({
            'success': True,
            'lead_id': lead.id,
            'message': 'Lead created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@leads_bp.route('/', methods=['GET'])
def get_leads():
    """Pobierz listę leadów z filtrowaniem"""
    try:
        # Parametry
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        source = request.args.get('source')
        
        # Query z filtrami
        query = Lead.query
        
        if status:
            query = query.filter_by(status=status)
        if source:
            query = query.filter_by(source=source)
        
        # Paginacja
        leads = query.order_by(
            Lead.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'page': page,
            'per_page': per_page,
            'total': leads.total,
            'pages': leads.pages,
            'leads': [lead.to_dict() for lead in leads.items]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@leads_bp.route('/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Pobierz szczegóły pojedynczego leadu"""
    try:
        lead = Lead.query.get(lead_id)
        
        if not lead:
            return jsonify({
                'success': False,
                'error': 'Lead not found'
            }), 404
        
        return jsonify({
            'success': True,
            'lead': lead.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@leads_bp.route('/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id):
    """Zaktualizuj status leadu"""
    try:
        lead = Lead.query.get(lead_id)
        
        if not lead:
            return jsonify({
                'success': False,
                'error': 'Lead not found'
            }), 404
        
        data = request.get_json()
        
        # Aktualizuj dozwolone pola
        if 'status' in data:
            lead.status = data['status']
        if 'notes' in data:
            lead.notes = data.get('notes')
        
        lead.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Lead updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500