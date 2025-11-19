"""
File Upload API Routes
======================
Image upload with optimization
"""

from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename

file_upload_routes = Blueprint("file_upload_routes", __name__)


# Rate limiting decorator
def rate_limit_upload(f):
    """Rate limit: 10 uploads per minute"""
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            from src.services.redis_rate_limiter import rate_limit_redis

            # Apply 10 uploads/min limit
            return rate_limit_redis(limit=10, window=60)(f)(*args, **kwargs)
        except (ImportError, ConnectionError, Exception) as e:
            # Fallback: no rate limiting if Redis unavailable
            print(f"⚠️ Rate limiter unavailable: {e}")
            return f(*args, **kwargs)

    return decorated_function


@file_upload_routes.route("/api/upload/image", methods=["POST"])
@rate_limit_upload
def upload_image():
    """
    Upload and optimize image

    Form data:
        file: Image file
        folder: Target folder (default: 'general')
        variants: Create variants (default: true)

    Returns:
        JSON with upload URLs
    """
    try:
        from src.services.file_upload_service import file_upload_service

        # Check if file in request
        if "file" not in request.files:
            return jsonify({"success": False, "error": "No file provided"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"success": False, "error": "Empty filename"}), 400

        # Get parameters
        folder = request.form.get("folder", "general")
        create_variants = request.form.get("variants", "true").lower() == "true"

        # Read file bytes
        file_bytes = file.read()
        filename = secure_filename(file.filename)

        # Upload
        result = file_upload_service.upload_file(
            file_bytes=file_bytes, filename=filename, folder=folder, create_variants=create_variants
        )

        return jsonify({"success": True, "message": "File uploaded successfully", "data": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@file_upload_routes.route("/api/upload/multiple", methods=["POST"])
@rate_limit_upload
def upload_multiple_images():
    """
    Upload multiple images

    Form data:
        files[]: Multiple image files
        folder: Target folder

    Returns:
        JSON with upload results
    """
    try:
        from src.services.file_upload_service import file_upload_service
        from werkzeug.utils import secure_filename

        # Check if files in request
        if "files[]" not in request.files:
            return jsonify({"success": False, "error": "No files provided"}), 400

        files = request.files.getlist("files[]")
        folder = request.form.get("folder", "general")

        results = []

        for file in files:
            if file.filename == "":
                continue

            try:
                file_bytes = file.read()
                filename = secure_filename(file.filename)

                result = file_upload_service.upload_file(
                    file_bytes=file_bytes, filename=filename, folder=folder, create_variants=True
                )

                results.append({"filename": filename, "success": True, "data": result})

            except Exception as e:
                results.append({"filename": file.filename, "success": False, "error": str(e)})

        return jsonify(
            {"success": True, "message": f"Uploaded {len(results)} files", "results": results}
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@file_upload_routes.route("/api/upload/delete", methods=["POST"])
def delete_file():
    """
    Delete uploaded file

    Body:
        {
            "filepath": "path/to/file.jpg"
        }

    Returns:
        JSON with deletion status
    """
    try:
        from src.services.file_upload_service import file_upload_service

        data = request.get_json()
        filepath = data.get("filepath")

        if not filepath:
            return jsonify({"success": False, "error": "filepath required"}), 400

        # Delete file
        file_upload_service.delete_file(filepath)

        return jsonify({"success": True, "message": "File deleted successfully"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
