"""
Entity management endpoints
"""

import json

from flask import Blueprint, jsonify

from src.models.chatbot import Entity

entities_bp = Blueprint("entities", __name__)


@entities_bp.route("/", methods=["GET"])
def get_entities():
    """Pobierz listę wszystkich encji"""
    try:
        entities = Entity.query.all()

        return jsonify(
            {
                "success": True,
                "count": len(entities),
                "entities": [
                    {
                        "id": entity.id,
                        "name": entity.name,
                        "values_count": len(json.loads(entity.values)) if entity.values else 0,
                        "created_at": entity.created_at.isoformat() if entity.created_at else None,
                    }
                    for entity in entities
                ],
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@entities_bp.route("/<int:entity_id>", methods=["GET"])
def get_entity(entity_id):
    """Pobierz szczegóły encji"""
    try:
        entity = Entity.query.get(entity_id)

        if not entity:
            return jsonify({"success": False, "error": "Entity not found"}), 404

        return jsonify({"success": True, "entity": entity.to_dict()})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
