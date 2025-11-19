"""
A/B Testing API Routes
======================
Experiment management and results API
"""

from flask import Blueprint, request, jsonify
from src.services.ab_testing_service import ABTestingService
from src.models.ab_testing import Experiment
from src.middleware.security import require_api_key

ab_testing_bp = Blueprint("ab_testing", __name__)


@ab_testing_bp.route("/experiments", methods=["POST"])
@require_api_key
def create_experiment():
    """
    Create new A/B test experiment
    POST /api/ab-testing/experiments

    Body:
    {
        "name": "Greeting Variant Test",
        "description": "Test different greeting messages",
        "experiment_type": "greeting",
        "variants": [
            {"id": "A", "name": "Control", "content": "Cześć! Jestem asystentem NovaHouse..."},
            {"id": "B", "name": "Variant B", "content": "Witaj! Pomogę Ci..."}
        ],
        "traffic_allocation": 0.5,
        "primary_metric": "conversion_rate",
        "min_sample_size": 100
    }
    """
    try:
        data = request.get_json()

        required_fields = ["name", "experiment_type", "variants"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        experiment = ABTestingService.create_experiment(
            name=data["name"],
            description=data.get("description", ""),
            experiment_type=data["experiment_type"],
            variants=data["variants"],
            traffic_allocation=data.get("traffic_allocation", 1.0),
            primary_metric=data.get("primary_metric", "conversion_rate"),
            min_sample_size=data.get("min_sample_size", 100),
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Experiment created successfully",
                    "experiment": experiment.to_dict(),
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@ab_testing_bp.route("/experiments", methods=["GET"])
@require_api_key
def list_experiments():
    """
    List all experiments
    GET /api/ab-testing/experiments?status=active
    """
    try:
        status = request.args.get("status")

        if status:
            experiments = Experiment.query.filter_by(status=status).all()
        else:
            experiments = Experiment.query.all()

        return (
            jsonify(
                {
                    "status": "success",
                    "experiments": [exp.to_dict() for exp in experiments],
                    "count": len(experiments),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@ab_testing_bp.route("/experiments/<int:experiment_id>", methods=["GET"])
@require_api_key
def get_experiment(experiment_id):
    """
    Get experiment details
    GET /api/ab-testing/experiments/{id}
    """
    try:
        experiment = Experiment.query.get(experiment_id)

        if not experiment:
            return jsonify({"error": "Experiment not found"}), 404

        return jsonify({"status": "success", "experiment": experiment.to_dict()}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@ab_testing_bp.route("/experiments/<int:experiment_id>/start", methods=["POST"])
@require_api_key
def start_experiment(experiment_id):
    """
    Start an experiment
    POST /api/ab-testing/experiments/{id}/start
    """
    try:
        result = ABTestingService.start_experiment(experiment_id)

        if "error" in result:
            return jsonify({"status": "error", "error": result["error"]}), 400

        return jsonify({"status": "success", **result}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@ab_testing_bp.route("/experiments/<int:experiment_id>/stop", methods=["POST"])
@require_api_key
def stop_experiment(experiment_id):
    """
    Stop an experiment and declare winner
    POST /api/ab-testing/experiments/{id}/stop
    """
    try:
        result = ABTestingService.stop_experiment(experiment_id)

        if "error" in result:
            return jsonify({"status": "error", "error": result["error"]}), 400

        return jsonify({"status": "success", **result}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@ab_testing_bp.route("/experiments/<int:experiment_id>/results", methods=["GET"])
@require_api_key
def get_experiment_results(experiment_id):
    """
    Get experiment results with statistical analysis
    GET /api/ab-testing/experiments/{id}/results
    """
    try:
        results = ABTestingService.get_experiment_results(experiment_id)

        if "error" in results:
            return jsonify({"status": "error", "error": results["error"]}), 404

        return jsonify({"status": "success", **results}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@ab_testing_bp.route("/assign", methods=["POST"])
def assign_variant():
    """
    Assign user to experiment variant (public endpoint for widget)
    POST /api/ab-testing/assign

    Body:
    {
        "experiment_id": 1,
        "session_id": "abc123",
        "user_id": "user_456"  // optional
    }
    """
    try:
        data = request.get_json()

        experiment_id = data.get("experiment_id")
        session_id = data.get("session_id")
        user_id = data.get("user_id", "anonymous")

        if not experiment_id or not session_id:
            return jsonify({"error": "experiment_id and session_id required"}), 400

        variant = ABTestingService.assign_variant(experiment_id, session_id, user_id)

        if not variant:
            return (
                jsonify({"status": "no_assignment", "message": "User not assigned to experiment"}),
                200,
            )

        return jsonify({"status": "success", "variant": variant}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@ab_testing_bp.route("/track/conversion", methods=["POST"])
def track_conversion():
    """
    Track conversion event
    POST /api/ab-testing/track/conversion

    Body:
    {
        "experiment_id": 1,
        "session_id": "abc123",
        "value": 1.0  // optional
    }
    """
    try:
        data = request.get_json()

        experiment_id = data.get("experiment_id")
        session_id = data.get("session_id")
        value = data.get("value", 1.0)

        if not experiment_id or not session_id:
            return jsonify({"error": "experiment_id and session_id required"}), 400

        ABTestingService.record_conversion(session_id, experiment_id, value)

        return jsonify({"status": "success", "message": "Conversion recorded"}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@ab_testing_bp.route("/track/engagement", methods=["POST"])
def track_engagement():
    """
    Track engagement metrics
    POST /api/ab-testing/track/engagement

    Body:
    {
        "experiment_id": 1,
        "session_id": "abc123",
        "messages": 5,
        "duration": 180  // seconds
    }
    """
    try:
        data = request.get_json()

        experiment_id = data.get("experiment_id")
        session_id = data.get("session_id")
        messages = data.get("messages", 0)
        duration = data.get("duration", 0)

        if not experiment_id or not session_id:
            return jsonify({"error": "experiment_id and session_id required"}), 400

        ABTestingService.record_engagement(session_id, experiment_id, messages, duration)

        return jsonify({"status": "success", "message": "Engagement recorded"}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@ab_testing_bp.route("/active", methods=["GET"])
def list_active_experiments():
    """
    List active experiments (public endpoint for widget)
    GET /api/ab-testing/active
    """
    try:
        experiments = ABTestingService.list_active_experiments()

        return (
            jsonify({"status": "success", "experiments": experiments, "count": len(experiments)}),
            200,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
