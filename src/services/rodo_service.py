"""
RODO/GDPR Service
Handles data inventory, retention, anonymization, and user rights (export/delete).
"""
import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from src.models.chatbot import ChatConversation, ChatMessage, Lead, db

logger = logging.getLogger(__name__)

# Configuration
DATA_RETENTION_MONTHS = int(os.getenv("DATA_RETENTION_MONTHS", "12"))  # 12 months default
ANONYMIZATION_THRESHOLD_MONTHS = int(os.getenv("ANONYMIZATION_THRESHOLD_MONTHS", "6"))  # Anonymize after 6 months


class RodoService:
    """
    Service for RODO/GDPR compliance:
    - Data inventory
    - Retention management
    - Anonymization
    - User rights (export/delete)
    """
    
    @staticmethod
    def get_data_inventory() -> Dict:
        """
        Get inventory of all personal data collected.
        
        Returns:
            Dict with data inventory
        """
        return {
            "personal_data_categories": {
                "name": {
                    "collected": True,
                    "purpose": "Personalization and lead identification",
                    "retention_months": DATA_RETENTION_MONTHS,
                    "storage": ["database", "backups", "monday.com"],
                },
                "email": {
                    "collected": True,
                    "purpose": "Contact and lead management",
                    "retention_months": DATA_RETENTION_MONTHS,
                    "storage": ["database", "backups", "monday.com", "email_service"],
                },
                "phone": {
                    "collected": True,
                    "purpose": "Contact and lead management",
                    "retention_months": DATA_RETENTION_MONTHS,
                    "storage": ["database", "backups", "monday.com"],
                },
                "chat_history": {
                    "collected": True,
                    "purpose": "Customer service and analytics",
                    "retention_months": DATA_RETENTION_MONTHS,
                    "storage": ["database", "backups"],
                },
                "files": {
                    "collected": True,
                    "purpose": "Project documentation",
                    "retention_months": DATA_RETENTION_MONTHS,
                    "storage": ["google_cloud_storage", "backups"],
                },
            },
            "legal_basis": [
                "Consent (RODO art. 6 ust. 1 lit. a)",
                "Contract performance (RODO art. 6 ust. 1 lit. b)",
            ],
            "user_rights": [
                "Right to access (art. 15)",
                "Right to rectification (art. 16)",
                "Right to erasure (art. 17)",
                "Right to data portability (art. 20)",
                "Right to object (art. 21)",
            ],
        }
    
    @staticmethod
    def anonymize_conversation(conversation_id: int) -> bool:
        """
        Anonymize a conversation by removing personal data.
        
        Args:
            conversation_id: ID of conversation to anonymize
            
        Returns:
            True if successful
        """
        try:
            conversation = ChatConversation.query.get(conversation_id)
            if not conversation:
                return False
            
            # Anonymize context_data
            context_data = json.loads(conversation.context_data or "{}")
            if "name" in context_data:
                context_data["name"] = "[ANONYMIZED]"
            if "email" in context_data:
                context_data["email"] = "[ANONYMIZED]"
            if "phone" in context_data:
                context_data["phone"] = "[ANONYMIZED]"
            conversation.context_data = json.dumps(context_data)
            
            # Anonymize email column (if exists)
            try:
                if hasattr(conversation, 'email') and conversation.email:
                    conversation.email = "[ANONYMIZED]"
            except Exception as e:
                # Column might not exist in database yet
                logger.debug(f"Email column not available for anonymization: {e}")
            
            # Mark as anonymized
            context_data["anonymized_at"] = datetime.now(timezone.utc).isoformat()
            conversation.context_data = json.dumps(context_data)
            
            # Anonymize messages
            messages = ChatMessage.query.filter_by(conversation_id=conversation_id).all()
            for message in messages:
                # Remove email/phone patterns from messages
                import re
                message.message = re.sub(
                    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                    '[EMAIL_REDACTED]',
                    message.message
                )
                message.message = re.sub(
                    r'\+?\d{1,3}[\s\-]?\d{3,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}',
                    '[PHONE_REDACTED]',
                    message.message
                )
            
            db.session.commit()
            logger.info(f"✅ Anonymized conversation {conversation_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error anonymizing conversation {conversation_id}: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    def anonymize_old_conversations(older_than_months: Optional[int] = None) -> Dict:
        """
        Anonymize conversations older than threshold.
        
        Args:
            older_than_months: Optional threshold in months (defaults to ANONYMIZATION_THRESHOLD_MONTHS)
        
        Returns:
            Dict with anonymization stats
        """
        try:
            threshold = older_than_months if older_than_months is not None else ANONYMIZATION_THRESHOLD_MONTHS
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=threshold * 30)
            
            old_conversations = (
                ChatConversation.query
                .filter(
                    ChatConversation.started_at < cutoff_date,
                    ChatConversation.ended_at.isnot(None)  # Only ended conversations
                )
                .all()
            )
            
            anonymized_count = 0
            for conversation in old_conversations:
                # Check if already anonymized
                context_data = json.loads(conversation.context_data or "{}")
                if context_data.get("anonymized_at"):
                    continue
                
                if RodoService.anonymize_conversation(conversation.id):
                    anonymized_count += 1
            
            logger.info(f"✅ Anonymized {anonymized_count} old conversations")
            
            return {
                "anonymized_count": anonymized_count,
                "cutoff_date": cutoff_date.isoformat(),
                "threshold_months": threshold,
            }
            
        except Exception as e:
            logger.error(f"Error anonymizing old conversations: {e}")
            return {
                "anonymized_count": 0,
                "error": str(e),
            }
    
    @staticmethod
    def export_user_data(user_identifier: str) -> Optional[Dict]:
        """
        Export all data for a user (GDPR right to data portability).
        Supports both email and session_id as identifier.
        
        Args:
            user_identifier: User's email address or session_id
            
        Returns:
            Dict with all user data or None if not found
        """
        try:
            # Try to find conversations by email (if column exists) or by session_id
            # Fallback: search in context_data JSON if email column doesn't exist
            conversations = []
            try:
                # First try: direct email column (if exists)
                # Search in context_data since email column doesn't exist
                conversations = ChatConversation.query.filter(
                    ChatConversation.context_data.like(f'%"email":"{user_identifier}"%')
                ).all()
            except Exception as e:
                # If email column doesn't exist, search in context_data
                logger.warning(f"Email column not available, searching in context_data: {e}")
                all_conversations = ChatConversation.query.all()
                for conv in all_conversations:
                    try:
                        context_data = json.loads(conv.context_data or "{}")
                        if context_data.get("email") == user_identifier or conv.session_id == user_identifier:
                            conversations.append(conv)
                    except:
                        if conv.session_id == user_identifier:
                            conversations.append(conv)
            
            # Also try session_id if no conversations found
            if not conversations:
                conversations = ChatConversation.query.filter_by(session_id=user_identifier).all()
            
            # Find all leads
            leads = Lead.query.filter_by(email=user_identifier).all()
            
            if not conversations and not leads:
                return None
            
            # Build export data
            export_data = {
                "user_identifier": user_identifier,
                "exported_at": datetime.now(timezone.utc).isoformat(),
                "conversations": [],
                "leads": [],
            }
            
            for conversation in conversations:
                messages = ChatMessage.query.filter_by(conversation_id=conversation.id).all()
                export_data["conversations"].append({
                    "session_id": conversation.session_id,
                    "started_at": conversation.started_at.isoformat(),
                    "ended_at": conversation.ended_at.isoformat() if conversation.ended_at else None,
                    "context_data": json.loads(conversation.context_data or "{}"),
                    "messages": [
                        {
                            "sender": msg.sender,
                            "message": msg.message,
                            "timestamp": msg.timestamp.isoformat(),
                        }
                        for msg in messages
                    ],
                })
            
            for lead in leads:
                export_data["leads"].append({
                    "id": lead.id,
                    "name": lead.name,
                    "email": lead.email,
                    "phone": lead.phone,
                    "message": lead.message,
                    "status": lead.status,
                    "created_at": lead.created_at.isoformat(),
                })
            
            return export_data
            
        except Exception as e:
            logger.error(f"Error exporting data for {user_identifier}: {e}")
            return None
    
    @staticmethod
    def delete_user_data(user_identifier: str) -> Dict:
        """
        Delete all data for a user (GDPR right to erasure).
        Supports both email and session_id as identifier.
        
        Args:
            user_identifier: User's email address or session_id
            
        Returns:
            Dict with deletion stats
        """
        try:
            deleted_conversations = 0
            deleted_leads = 0
            
            # Delete conversations - try email column first, fallback to session_id and context_data
            conversations = []
            try:
                # First try: direct email column (if exists)
                # Search in context_data since email column doesn't exist
                conversations = ChatConversation.query.filter(
                    ChatConversation.context_data.like(f'%"email":"{user_identifier}"%')
                ).all()
            except Exception as e:
                # If email column doesn't exist, search in context_data
                logger.warning(f"Email column not available, searching in context_data: {e}")
                all_conversations = ChatConversation.query.all()
                for conv in all_conversations:
                    try:
                        context_data = json.loads(conv.context_data or "{}")
                        if context_data.get("email") == user_identifier or conv.session_id == user_identifier:
                            conversations.append(conv)
                    except:
                        if conv.session_id == user_identifier:
                            conversations.append(conv)
            
            # Also try session_id if no conversations found
            if not conversations:
                conversations = ChatConversation.query.filter_by(session_id=user_identifier).all()
            
            for conversation in conversations:
                # Delete messages (cascade should handle this, but explicit for safety)
                ChatMessage.query.filter_by(conversation_id=conversation.id).delete()
                db.session.delete(conversation)
                deleted_conversations += 1
            
            # Delete leads
            leads = Lead.query.filter_by(email=user_identifier).all()
            for lead in leads:
                db.session.delete(lead)
                deleted_leads += 1
            
            db.session.commit()
            
            logger.info(f"✅ Deleted all data for {user_identifier}: {deleted_conversations} conversations, {deleted_leads} leads")
            
            return {
                "user_identifier": user_identifier,
                "deleted_conversations": deleted_conversations,
                "deleted_leads": deleted_leads,
                "deleted_at": datetime.now(timezone.utc).isoformat(),
            }
            
        except Exception as e:
            logger.error(f"Error deleting data for {user_identifier}: {e}")
            db.session.rollback()
            return {
                "user_identifier": user_identifier,
                "error": str(e),
            }


# Global instance
rodo_service = RodoService()

