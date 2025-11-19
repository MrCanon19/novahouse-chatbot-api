"""
I18n API Routes
===============
Multi-language support endpoints
"""

from flask import Blueprint, jsonify, request

from src.services.i18n_service import I18nService

i18n_bp = Blueprint("i18n", __name__)


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
    Translate a key to target language
    POST /api/i18n/translate

    Body:
    {
        "key": "greeting",
        "language": "en"
    }
    """
    try:
        data = request.get_json()
        key = data.get("key", "")
        language = data.get("language", I18nService.DEFAULT_LANGUAGE)

        if not key:
            return jsonify({"error": "Key is required"}), 400

        translation = I18nService.translate(key, language)

        return (
            jsonify(
                {"status": "success", "key": key, "language": language, "translation": translation}
            ),
            200,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@i18n_bp.route("/languages", methods=["GET"])
def get_supported_languages():
    """
    Get list of supported languages
    GET /api/i18n/languages
    """
    try:
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
def get_faq_translation(intent, language):
    """
    Get FAQ translation for specific intent and language
    GET /api/i18n/faq/{intent}/{language}
    """
    try:
        if language not in I18nService.SUPPORTED_LANGUAGES:
            supported = ", ".join(I18nService.SUPPORTED_LANGUAGES)
            return (
                jsonify({"error": f"Unsupported language. Supported: {supported}"}),
                400,
            )

        translation = I18nService.translate_faq(intent, language)

        if not translation:
            return (
                jsonify(
                    {"status": "not_found", "message": f"No translation found for intent: {intent}"}
                ),
                404,
            )

        return (
            jsonify(
                {
                    "status": "success",
                    "intent": intent,
                    "language": language,
                    "translation": translation,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
