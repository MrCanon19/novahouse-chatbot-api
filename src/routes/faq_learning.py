"""
FAQ Learning Routes
===================
Admin endpoints for managing learned FAQs
"""

from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from src.models.chatbot import db
from src.models.faq_learning import LearnedFAQ, UnknownQuestion
from src.middleware.security import require_auth

faq_learning_routes = Blueprint("faq_learning", __name__, url_prefix="/api/faq-learning")

# All FAQ learning endpoints require authentication
faq_learning_routes.before_request(require_auth)


@faq_learning_routes.route("/unknown", methods=["GET"])
def get_unknown_questions():
    """Get all unknown/unanswered questions"""
    try:
        status = request.args.get("status", "pending")
        limit = int(request.args.get("limit", 50))

        query = UnknownQuestion.query

        if status != "all":
            query = query.filter_by(status=status)

        questions = query.order_by(UnknownQuestion.created_at.desc()).limit(limit).all()

        return jsonify({"questions": [q.to_dict() for q in questions], "count": len(questions)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@faq_learning_routes.route("/unknown/<int:question_id>", methods=["PUT"])
def update_unknown_question(question_id):
    """Update status of unknown question"""
    try:
        data = request.get_json()
        question = UnknownQuestion.query.get_or_404(question_id)

        if "status" in data:
            question.status = data["status"]
        if "admin_notes" in data:
            question.admin_notes = data["admin_notes"]
        if "category" in data:
            question.category = data["category"]

        question.reviewed_at = datetime.now(timezone.utc)
        question.reviewed_by = data.get("reviewed_by", "admin")

        db.session.commit()

        return jsonify({"message": "Question updated", "question": question.to_dict()})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@faq_learning_routes.route("/learned", methods=["GET"])
def get_learned_faqs():
    """Get all learned FAQ entries"""
    try:
        is_active = request.args.get("active", "true").lower() == "true"

        faqs = (
            LearnedFAQ.query.filter_by(is_active=is_active)
            .order_by(LearnedFAQ.usage_count.desc())
            .all()
        )

        return jsonify({"faqs": [faq.to_dict() for faq in faqs], "count": len(faqs)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@faq_learning_routes.route("/learned", methods=["POST"])
def create_learned_faq():
    """Create new learned FAQ entry"""
    try:
        data = request.get_json()

        if not data or "question_pattern" not in data or "answer" not in data:
            return jsonify({"error": "question_pattern and answer are required"}), 400

        # Validate input types and lengths
        question_pattern = data["question_pattern"]
        answer = data["answer"]
        if not isinstance(question_pattern, str) or not (1 <= len(question_pattern) <= 500):
            return jsonify({"error": "Invalid question_pattern"}), 400
        if not isinstance(answer, str) or not (1 <= len(answer) <= 5000):
            return jsonify({"error": "Invalid answer"}), 400
        category = data.get("category")
        if category and (not isinstance(category, str) or len(category) > 100):
            return jsonify({"error": "Invalid category"}), 400

        faq = LearnedFAQ(
            question_pattern=question_pattern.strip(),
            answer=answer.strip(),
            category=category.strip() if category else None,
            created_by=data.get("created_by", "admin"),
        )

        db.session.add(faq)
        db.session.commit()

        return jsonify({"message": "FAQ created", "faq": faq.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        import logging

        logging.getLogger(__name__).error(f"FAQ creation failed: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@faq_learning_routes.route("/learned/<int:faq_id>", methods=["PUT"])
def update_learned_faq(faq_id):
    """Update learned FAQ entry"""
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid payload"}), 400

        faq = LearnedFAQ.query.get_or_404(faq_id)

        if "question_pattern" in data:
            qp = data["question_pattern"]
            if not isinstance(qp, str) or not (1 <= len(qp) <= 500):
                return jsonify({"error": "Invalid question_pattern"}), 400
            faq.question_pattern = qp.strip()
        if "answer" in data:
            ans = data["answer"]
            if not isinstance(ans, str) or not (1 <= len(ans) <= 5000):
                return jsonify({"error": "Invalid answer"}), 400
            faq.answer = ans.strip()
        if "category" in data:
            cat = data["category"]
            if cat and (not isinstance(cat, str) or len(cat) > 100):
                return jsonify({"error": "Invalid category"}), 400
            faq.category = cat.strip() if cat else None
        if "is_active" in data:
            if not isinstance(data["is_active"], bool):
                return jsonify({"error": "Invalid is_active"}), 400
            faq.is_active = data["is_active"]

        db.session.commit()

        return jsonify({"message": "FAQ updated", "faq": faq.to_dict()})

    except Exception as e:
        db.session.rollback()
        import logging

        logging.getLogger(__name__).error(f"FAQ update failed: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@faq_learning_routes.route("/learned/<int:faq_id>", methods=["DELETE"])
def delete_learned_faq(faq_id):
    """Delete learned FAQ entry"""
    try:
        faq = LearnedFAQ.query.get_or_404(faq_id)
        db.session.delete(faq)
        db.session.commit()

        return jsonify({"message": "FAQ deleted"})

    except Exception as e:
        db.session.rollback()
        import logging

        logging.getLogger(__name__).error(f"FAQ deletion failed: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@faq_learning_routes.route("/stats", methods=["GET"])
def get_learning_stats():
    """Get FAQ learning statistics"""
    try:
        total_unknown = UnknownQuestion.query.count()
        pending_review = UnknownQuestion.query.filter_by(status="pending").count()
        added_to_faq = UnknownQuestion.query.filter_by(status="added_to_faq").count()
        total_learned = LearnedFAQ.query.filter_by(is_active=True).count()

        # Most used learned FAQs
        top_faqs = (
            LearnedFAQ.query.filter_by(is_active=True)
            .order_by(LearnedFAQ.usage_count.desc())
            .limit(10)
            .all()
        )

        return jsonify(
            {
                "total_unknown_questions": total_unknown,
                "pending_review": pending_review,
                "added_to_faq": added_to_faq,
                "total_learned_faqs": total_learned,
                "top_learned_faqs": [faq.to_dict() for faq in top_faqs],
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@faq_learning_routes.route("/feedback", methods=["POST"])
def submit_feedback():
    """Submit user feedback on bot response"""
    try:
        data = request.get_json()

        if not data or "session_id" not in data or "question" not in data:
            return jsonify({"error": "session_id and question are required"}), 400

        # Check if question already logged
        existing = UnknownQuestion.query.filter_by(
            session_id=data["session_id"], question=data["question"]
        ).first()

        if existing:
            if "was_helpful" in data:
                existing.was_helpful = data["was_helpful"]
            if "user_feedback" in data:
                existing.user_feedback = data["user_feedback"]
            db.session.commit()
            return jsonify({"message": "Feedback updated"})

        # Create new entry
        unknown = UnknownQuestion(
            session_id=data["session_id"],
            question=data["question"],
            bot_response=data.get("bot_response"),
            was_helpful=data.get("was_helpful"),
            user_feedback=data.get("user_feedback"),
        )

        db.session.add(unknown)
        db.session.commit()

        return jsonify({"message": "Feedback submitted"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@faq_learning_routes.route("/auto-learn", methods=["POST"])
def auto_learn_from_questions():
    """
    Automatycznie dodaje do FAQ pytania które wiele osób zadaje
    Wymaga: min 3 osoby zadały podobne pytanie
    """
    try:
        from sqlalchemy import func
        from difflib import SequenceMatcher

        # Pobierz wszystkie pending questions
        pending_questions = UnknownQuestion.query.filter_by(status="pending").all()

        # Grupuj podobne pytania (używając podobieństwa tekstowego)
        question_groups = {}
        for question in pending_questions:
            # Znajdź podobne pytania
            matched = False
            for existing_key in question_groups.keys():
                similarity = SequenceMatcher(None, question.question.lower(), existing_key.lower()).ratio()
                if similarity > 0.7:  # 70% podobieństwa
                    question_groups[existing_key].append(question)
                    matched = True
                    break

            if not matched:
                question_groups[question.question] = [question]

        # Dodaj do FAQ jeśli grupa ma >= 3 pytania
        learned_count = 0
        for question_text, questions in question_groups.items():
            if len(questions) >= 3:
                # Sprawdź czy już nie ma takiego FAQ
                existing_faq = LearnedFAQ.query.filter_by(
                    question_pattern=question_text[:200]  # Max 200 chars
                ).first()

                if not existing_faq:
                    # Użyj najczęstszej odpowiedzi jako wzorca
                    bot_responses = [q.bot_response for q in questions if q.bot_response]
                    if bot_responses:
                        most_common_response = max(set(bot_responses), key=bot_responses.count)

                        # Utwórz nowy FAQ
                        new_faq = LearnedFAQ(
                            question_pattern=question_text[:200],
                            answer=most_common_response[:5000] if most_common_response else "Brak odpowiedzi",
                            category="auto-learned",
                            created_by="auto-learning-system",
                        )
                        db.session.add(new_faq)

                        # Oznacz pytania jako dodane do FAQ
                        for q in questions:
                            q.status = "added_to_faq"
                            q.reviewed_at = datetime.now(timezone.utc)
                            q.reviewed_by = "auto-learning-system"

                        learned_count += 1

        db.session.commit()

        return jsonify(
            {
                "message": f"Auto-learned {learned_count} new FAQs",
                "learned_count": learned_count,
                "total_groups": len(question_groups),
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
