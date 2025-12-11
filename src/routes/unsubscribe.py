"""
Unsubscribe routes for RODO/GDPR compliance.

Endpoints:
- POST /api/unsubscribe - Unsubscribe from marketing emails
- POST /api/revoke-consent - Revoke all data processing consent
- GET /api/unsubscribe/status/<email> - Check unsubscribe status
"""

import logging
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from src.models.chatbot import ChatConversation, Lead, db
from src.models.consent_audit_log import ConsentAuditLog

logger = logging.getLogger(__name__)

unsubscribe_bp = Blueprint("unsubscribe", __name__)


def _get_client_ip() -> str:
    """Extract client IP from request (handles proxies)"""
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0].strip()
    return request.remote_addr or "unknown"


@unsubscribe_bp.route("/api/unsubscribe", methods=["POST"])
def unsubscribe():
    """
    Unsubscribe from marketing emails.

    Request body:
    {
        "email": "user@example.com",  # OR
        "conversation_id": 123,       # OR
        "lead_id": 456,
        "reason": "Too many emails"   # Optional
    }

    RODO Compliance: Sets marketing_consent=False, logs action in audit trail.
    """
    try:
        payload = request.get_json(silent=True) or {}

        email = payload.get("email", "").strip()
        conversation_id = payload.get("conversation_id")
        lead_id = payload.get("lead_id")
        reason = payload.get("reason", "").strip()

        if not (email or conversation_id or lead_id):
            return jsonify({"error": "Must provide email, conversation_id, or lead_id"}), 400

        # Find and update conversation
        if conversation_id:
            conversation = ChatConversation.query.get(conversation_id)
            if conversation:
                conversation.marketing_consent = False
                conversation.rodo_consent = False
                email = email or conversation.email or "unknown"
                db.session.add(conversation)

        # Find and update lead
        if lead_id:
            lead = Lead.query.get(lead_id)
            if lead:
                lead.marketing_consent = False
                email = email or lead.email or "unknown"
                db.session.add(lead)

        # Find and update by email
        if email and email != "unknown":
            # Search in context_data since email column doesn't exist
            conversations = ChatConversation.query.filter(
                ChatConversation.context_data.like(f'%"email":"{email}"%')
            ).all()
            for conv in conversations:
                conv.marketing_consent = False
                db.session.add(conv)

            leads = Lead.query.filter_by(email=email).all()
            for lead in leads:
                lead.marketing_consent = False
                db.session.add(lead)

        # Log audit trail
        audit_log = ConsentAuditLog(
            conversation_id=conversation_id,
            lead_id=lead_id,
            email=email,
            action="unsubscribe",
            timestamp=datetime.now(timezone.utc),
            ip_address=_get_client_ip(),
            user_agent=request.headers.get("User-Agent", ""),
            reason=reason,
        )
        db.session.add(audit_log)
        db.session.commit()

        logger.info(f"✅ Unsubscribed: {email} (IP: {_get_client_ip()})")

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Successfully unsubscribed from marketing emails",
                    "email": email,
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Unsubscribe error: {e}", exc_info=True)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@unsubscribe_bp.route("/api/revoke-consent", methods=["POST"])
def revoke_consent():
    """
    Revoke ALL data processing consent (GDPR/RODO right to be forgotten).

    Request body:
    {
        "email": "user@example.com",
        "reason": "I want to delete my data"
    }

    Actions:
    1. Set rodo_consent=False (revoke processing consent)
    2. Set marketing_consent=False (revoke marketing)
    3. Log to ConsentAuditLog for audit trail
    4. Optionally: Schedule for deletion after 30 days
    """
    try:
        payload = request.get_json(silent=True) or {}

        email = payload.get("email", "").strip()
        reason = payload.get("reason", "").strip()

        if not email:
            return jsonify({"error": "Email is required"}), 400

        # Revoke all consents
        affected_count = 0

        conversations = ChatConversation.query.filter_by(email=email).all()
        for conv in conversations:
            conv.rodo_consent = False
            conv.marketing_consent = False
            db.session.add(conv)
            affected_count += 1

        leads = Lead.query.filter_by(email=email).all()
        for lead in leads:
            lead.marketing_consent = False
            db.session.add(lead)
            affected_count += 1

        # Log to audit trail
        audit_log = ConsentAuditLog(
            email=email,
            action="revoke-consent",
            timestamp=datetime.now(timezone.utc),
            ip_address=_get_client_ip(),
            user_agent=request.headers.get("User-Agent", ""),
            reason=reason,
            notes=f"Revoked all consents. Affected {affected_count} records.",
        )
        db.session.add(audit_log)
        db.session.commit()

        logger.warning(
            f"🔒 Consent revoked for {email}: {affected_count} records affected "
            f"(IP: {_get_client_ip()})"
        )

        return (
            jsonify(
                {
                    "success": True,
                    "message": "All consents revoked. Your data will not be processed.",
                    "email": email,
                    "affected_records": affected_count,
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Revoke consent error: {e}", exc_info=True)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@unsubscribe_bp.route("/api/unsubscribe/status/<email>", methods=["GET"])
def check_unsubscribe_status(email: str):
    """
    Check unsubscribe/consent status for an email address.

    Returns: {
        "email": "user@example.com",
        "is_unsubscribed": true,
        "marketing_consent": false,
        "rodo_consent": false,
        "last_action": "unsubscribe",
        "last_action_at": "2025-01-20T10:30:00Z"
    }
    """
    try:
        email = email.lower().strip()

        # Check latest action in audit log
        latest_log = (
            ConsentAuditLog.query.filter_by(email=email)
            .order_by(ConsentAuditLog.timestamp.desc())
            .first()
        )

        # Check conversation status
        # Search in context_data since email column doesn't exist
        conversation = ChatConversation.query.filter(
            ChatConversation.context_data.like(f'%"email":"{email}"%')
        ).first()
        lead = Lead.query.filter_by(email=email).first()

        marketing_consent = False
        rodo_consent = False

        if conversation:
            marketing_consent = conversation.marketing_consent
            rodo_consent = conversation.rodo_consent
        elif lead:
            marketing_consent = lead.marketing_consent

        return (
            jsonify(
                {
                    "email": email,
                    "is_unsubscribed": not marketing_consent,
                    "marketing_consent": marketing_consent,
                    "rodo_consent": rodo_consent,
                    "last_action": latest_log.action if latest_log else None,
                    "last_action_at": latest_log.timestamp.isoformat() if latest_log else None,
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Status check error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
