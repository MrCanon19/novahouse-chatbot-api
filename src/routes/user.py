from flask import Blueprint, current_app, jsonify, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.models.user import User, db

user_bp = Blueprint("user", __name__)


def _json_error(message: str, status: int = 400):
    return jsonify({"status": "error", "message": message}), status


def _safe_commit(context: str):
    try:
        db.session.commit()
        return None
    except IntegrityError:
        db.session.rollback()
        return _json_error("User with this username or email already exists", 409)
    except SQLAlchemyError as exc:  # pragma: no cover - defensive safety net
        db.session.rollback()
        current_app.logger.exception("users.commit.failed", extra={"context": context})
        return _json_error("Database error while saving user", 503)


@user_bp.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        return jsonify(
            {
                "status": "success",
                "count": len(users),
                "users": [user.to_dict() for user in users],
            }
        )
    except SQLAlchemyError as exc:
        current_app.logger.exception("users.list.failed", exc_info=exc)
        return jsonify(
            {
                "status": "success",
                "count": 0,
                "users": [],
                "warnings": ["Database unavailable, returning an empty list"],
            }
        )


@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True)

    if data is None and (request.data or not request.is_json):
        return _json_error("Invalid JSON payload", 400)

    data = data or {}
    if not isinstance(data, dict):
        return _json_error("Invalid JSON payload", 400)

    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()

    if not username or not email:
        return _json_error("Username and email are required", 400)

    user = User(username=username, email=email)
    db.session.add(user)

    commit_error = _safe_commit("create_user")
    if commit_error:
        return commit_error

    return jsonify({"status": "success", "user": user.to_dict()}), 201


@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
    except SQLAlchemyError as exc:
        current_app.logger.exception("users.get.failed", exc_info=exc)
        return jsonify(
            {
                "status": "error",
                "message": "Database error while retrieving user",
            }
        )

    if not user:
        return _json_error("User not found", 404)

    return jsonify({"status": "success", "user": user.to_dict()})


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
    except SQLAlchemyError as exc:
        current_app.logger.exception("users.update.fetch_failed", exc_info=exc)
        return _json_error("Database error while retrieving user", 503)

    if not user:
        return _json_error("User not found", 404)

    data = request.get_json(silent=True)
    if data is None and (request.data or not request.is_json):
        return _json_error("Invalid JSON payload", 400)

    data = data or {}
    if not isinstance(data, dict):
        return _json_error("Invalid JSON payload", 400)

    username = data.get("username")
    email = data.get("email")

    if username is None and email is None:
        return _json_error("Provide username or email to update", 400)

    if username is not None:
        user.username = username.strip() or user.username
    if email is not None:
        user.email = email.strip() or user.email

    commit_error = _safe_commit("update_user")
    if commit_error:
        return commit_error

    return jsonify({"status": "success", "user": user.to_dict()})


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
    except SQLAlchemyError as exc:
        current_app.logger.exception("users.delete.fetch_failed", exc_info=exc)
        return _json_error("Database error while retrieving user", 503)

    if not user:
        return _json_error("User not found", 404)

    try:
        db.session.delete(user)
        commit_error = _safe_commit("delete_user")
        if commit_error:
            return commit_error
    except SQLAlchemyError as exc:  # pragma: no cover - defensive safety net
        current_app.logger.exception("users.delete.failed", exc_info=exc)
        db.session.rollback()
        return _json_error("Database error while deleting user", 503)

    return "", 204
