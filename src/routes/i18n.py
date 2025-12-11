"""
I18n API Routes
===============
Multi-language support endpoints
"""

from flask import Blueprint, jsonify, request

# I18n service (optional - may not exist)
try:
    from src.services.i18n_service import I18nService
except ImportError:
    I18nService = None

i18n_bp = Blueprint("i18n", __name__)


def _check_i18n_service():
    """Check if I18nService is available"""
    if I18nService is None:
        return jsonify({"error": "I18n service not available"}), 503
    return None


@i18n_bp.route("/detect", methods=["POST"])
def detect_language():
    """
    Detect language from text
    POST /api/i18n/detect

    Body:
    {
        "text": "Witam, chciałbym zapytać o cennik"
    }
    """
    try:
        error_response = _check_i18n_service()
        if error_response:
            return error_response

        data = request.get_json()
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "Text is required"}), 400

        detected_lang = I18nService.detect_language(text)

        return jsonify({"status": "success", "detected_language": detected_lang, "text": text}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@i18n_bp.route("/translations/<language>", methods=["GET"])
def get_translations(language):
    """
    Get all translations for a language
    GET /api/i18n/translations/{language}
    """
    try:
        error_response = _check_i18n_service()
        if error_response:
            return error_response

        if language not in I18nService.SUPPORTED_LANGUAGES:
            supported = ", ".join(I18nService.SUPPORTED_LANGUAGES)
            return (
                jsonify({"error": f"Unsupported language. Supported: {supported}"}),
                400,
            )

        translations = I18nService.get_all_translations(language)

        return (
            jsonify({"status": "success", "language": language, "translations": translations}),
            200,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@i18n_bp.route("/translate", methods=["POST"])
def translate():
    """
    Translate a key to a language
    POST /api/i18n/translate

    Body:
    {
        "key": "greeting",
        "language": "pl"
    }
    """
    try:
        error_response = _check_i18n_service()
        if error_response:
            return error_response

        data = request.get_json()
        key = data.get("key")
        language = data.get("language", I18nService.DEFAULT_LANGUAGE)

        if not key:
            return jsonify({"error": "Key is required"}), 400

        translation = I18nService.translate(key, language)

        return jsonify({"status": "success", "key": key, "language": language, "translation": translation}), 200

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@i18n_bp.route("/languages", methods=["GET"])
def get_languages():
    """
    Get list of supported languages
    GET /api/i18n/languages
    """
    try:
        error_response = _check_i18n_service()
        if error_response:
            return error_response

        languages = I18nService.format_language_switcher()

        return (
            jsonify(
                {
                    "status": "success",
                    "languages": languages,
                    "default": I18nService.DEFAULT_LANGUAGE,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@i18n_bp.route("/faq/<intent>/<language>", methods=["GET"])
def translate_faq(intent, language):
    """
    Translate FAQ intent to a language
    GET /api/i18n/faq/{intent}/{language}
    """
    try:
        error_response = _check_i18n_service()
        if error_response:
            return error_response

        if language not in I18nService.SUPPORTED_LANGUAGES:
            supported = ", ".join(I18nService.SUPPORTED_LANGUAGES)
            return (
                jsonify({"error": f"Unsupported language. Supported: {supported}"}),
                400,
            )

        translation = I18nService.translate_faq(intent, language)

        return (
            jsonify({"status": "success", "intent": intent, "language": language, "translation": translation}),
            200,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
