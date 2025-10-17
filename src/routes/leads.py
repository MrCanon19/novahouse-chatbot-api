from flask import Blueprint, request, jsonify
from src.models.chatbot import db, Lead
from src.integrations.monday_client import MondayClient
from datetime import datetime

leads_bp = Blueprint('leads', __name__)

@leads_bp.route('/', methods=['POST'])
def create_lead():
    """Create a new lead"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        lead = Lead(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            message=data.get('message'),
            status='new',
            created_at=datetime.utcnow()
        )
        
        db.session.add(lead)
        db.session.commit()
        
        try:
            monday = MondayClient()
            monday_item_id = monday.create_lead_item({
                'name': lead.name,
                'email': lead.email,
                'phone': lead.phone,
                'message': lead.message
            })
            
            if monday_item_id:
                lead.monday_item_id = monday_item_id
                db.session.commit()
                print(f"Lead {lead.id} synced to Monday.com: {monday_item_id}")
        
        except Exception as e:
            print(f"Monday.com sync error: {e}")
        
        return jsonify({
            'id': lead.id,
            'name': lead.name,
            'email': lead.email,
            'phone': lead.phone,
            'message': lead.message,
            'status': lead.status,
            'monday_item_id': lead.monday_item_id,
            'created_at': lead.created_at.isoformat()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/', methods=['GET'])
def get_leads():
    """Get all leads"""
    try:
        leads = Lead.query.order_by(Lead.created_at.desc()).all()
        
        return jsonify([{
            'id': lead.id,
            'name': lead.name,
            'email': lead.email,
            'phone': lead.phone,
            'message': lead.message,
            'status': lead.status,
            'monday_item_id': lead.monday_item_id,
            'created_at': lead.created_at.isoformat()
        } for lead in leads]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    """Get a specific lead"""
    try:
        lead = Lead.query.get(lead_id)
        
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        return jsonify({
            'id': lead.id,
            'name': lead.name,
            'email': lead.email,
            'phone': lead.phone,
            'message': lead.message,
            'status': lead.status,
            'monday_item_id': lead.monday_item_id,
            'created_at': lead.created_at.isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@leads_bp.route('/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id):
    """Update a lead"""
    try:
        lead = Lead.query.get(lead_id)
        
        if not lead:
            return jsonify({'error': 'Lead not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            lead.name = data['name']
        if 'email' in data:
            lead.email = data['email']
        if 'phone' in data:
            lead.phone = data['phone']
        if 'message' in data:
            lead.message = data['message']
        if 'status' in data:
            lead.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'id': lead.id,
            'name': lead.name,
            'email': lead.email,
            'phone': lead.phone,
            'message': lead.message,
            'status': lead.status,
            'monday_item_id': lead.monday_item_id,
            'created_at': lead.created_at.isoformat()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
