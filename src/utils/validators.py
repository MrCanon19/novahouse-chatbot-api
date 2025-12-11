"""
Input Validation Utilities
Validates chat payloads, lead data, and file uploads.
"""
import os
from typing import Dict, Any, Tuple, Optional

from src.exceptions import (
    ValidationError,
    ChatMessageTooLongError,
    InvalidFileTypeError,
    FileTooLargeError,
)


# Limits
MAX_MESSAGE_LENGTH = 4000
MAX_PAYLOAD_SIZE_KB = 100  # 100 KB max JSON payload
MAX_PAYLOAD_KEYS = 50  # Max number of keys in JSON payload
MAX_FILE_SIZE_MB = 5  # 5 MB max file size

# Allowed MIME types for file uploads
ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/gif",
    "image/webp",
    "application/pdf",
    "text/plain",
    "application/msword",  # .doc
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
}

# Blocked MIME types (security)
BLOCKED_MIME_TYPES = {
    "image/svg+xml",  # SVG can contain JS
    "text/html",  # HTML can contain JS
    "application/javascript",
    "text/javascript",
    "application/x-javascript",
}


def validate_chat_payload(payload: Dict[str, Any]) -> Tuple[str, str]:
    """
    Validate chat message payload.
    
    Args:
        payload: JSON payload from request
        
    Returns:
        Tuple of (user_message, session_id)
        
    Raises:
        ValidationError: If validation fails
        ChatMessageTooLongError: If message is too long
    """
    # Check payload size (rough estimate)
    import json
    payload_size_kb = len(json.dumps(payload).encode("utf-8")) / 1024
    if payload_size_kb > MAX_PAYLOAD_SIZE_KB:
        raise ValidationError(
            f"Payload too large: {payload_size_kb:.1f} KB (max {MAX_PAYLOAD_SIZE_KB} KB)"
        )
    
    # Check number of keys
    if len(payload) > MAX_PAYLOAD_KEYS:
        raise ValidationError(
            f"Too many keys in payload: {len(payload)} (max {MAX_PAYLOAD_KEYS})"
        )
    
    # Validate message field
    raw_message = payload.get("message")
    if not isinstance(raw_message, str):
        raise ValidationError("Field 'message' must be a string")
    
    if not raw_message.strip():
        raise ValidationError("Field 'message' cannot be empty")
    
    user_message = raw_message.strip()
    
    # Check message length
    if len(user_message) > MAX_MESSAGE_LENGTH:
        raise ChatMessageTooLongError(
            f"Message exceeds maximum length: {len(user_message)} characters "
            f"(max {MAX_MESSAGE_LENGTH})"
        )
    
    # Validate session_id (optional)
    session_id = payload.get("session_id")
    if session_id is not None:
        if not isinstance(session_id, str):
            raise ValidationError("Field 'session_id' must be a string")
        if len(session_id) > 255:
            raise ValidationError("Field 'session_id' exceeds maximum length (255)")
    
    return user_message, session_id or ""


def validate_lead_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate lead creation payload.
    
    Args:
        payload: JSON payload with lead data
        
    Returns:
        Validated and sanitized payload
        
    Raises:
        ValidationError: If validation fails
    """
    # Check payload size
    import json
    payload_size_kb = len(json.dumps(payload).encode("utf-8")) / 1024
    if payload_size_kb > MAX_PAYLOAD_SIZE_KB:
        raise ValidationError(
            f"Payload too large: {payload_size_kb:.1f} KB (max {MAX_PAYLOAD_SIZE_KB} KB)"
        )
    
    # Required fields
    required_fields = ["email"]
    for field in required_fields:
        if field not in payload:
            raise ValidationError(f"Missing required field: {field}")
    
    # Validate email format (basic)
    email = payload.get("email", "")
    if not isinstance(email, str) or "@" not in email:
        raise ValidationError("Invalid email format")
    
    if len(email) > 255:
        raise ValidationError("Email exceeds maximum length (255)")
    
    # Validate optional fields
    if "name" in payload:
        name = payload["name"]
        if not isinstance(name, str):
            raise ValidationError("Field 'name' must be a string")
        if len(name) > 255:
            raise ValidationError("Field 'name' exceeds maximum length (255)")
    
    if "phone" in payload:
        phone = payload["phone"]
        if not isinstance(phone, str):
            raise ValidationError("Field 'phone' must be a string")
        if len(phone) > 50:
            raise ValidationError("Field 'phone' exceeds maximum length (50)")
    
    if "message" in payload:
        message = payload["message"]
        if not isinstance(message, str):
            raise ValidationError("Field 'message' must be a string")
        if len(message) > 5000:
            raise ValidationError("Field 'message' exceeds maximum length (5000)")
    
    return payload


def validate_uploaded_file(
    file,
    filename: Optional[str] = None,
    content_type: Optional[str] = None,
) -> Tuple[bytes, str, str]:
    """
    Validate uploaded file.
    
    Args:
        file: File object from request
        filename: Original filename (optional)
        content_type: MIME type (optional)
        
    Returns:
        Tuple of (file_content, validated_filename, validated_content_type)
        
    Raises:
        FileTooLargeError: If file exceeds size limit
        InvalidFileTypeError: If file type is not allowed
    """
    # Read file content
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    # Check file size
    file_size_mb = file_size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise FileTooLargeError(
            f"File exceeds maximum size: {file_size_mb:.2f} MB (max {MAX_FILE_SIZE_MB} MB)"
        )
    
    # Read content
    content = file.read()
    
    # Validate filename
    if not filename:
        filename = getattr(file, "filename", "upload")
    
    # Validate content type
    if not content_type:
        content_type = getattr(file, "content_type", "application/octet-stream")
    
    # Check blocked types
    if content_type in BLOCKED_MIME_TYPES:
        raise InvalidFileTypeError(
            f"File type '{content_type}' is not allowed for security reasons"
        )
    
    # Check allowed types
    if content_type not in ALLOWED_MIME_TYPES:
        raise InvalidFileTypeError(
            f"File type '{content_type}' is not allowed. "
            f"Allowed types: {', '.join(sorted(ALLOWED_MIME_TYPES))}"
        )
    
    # Additional security: check file extension matches MIME type
    filename_lower = filename.lower()
    extension_mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".pdf": "application/pdf",
        ".txt": "text/plain",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }
    
    # Get extension
    ext = None
    for ext_check in extension_mime_map:
        if filename_lower.endswith(ext_check):
            ext = ext_check
            break
    
    if ext and extension_mime_map[ext] != content_type:
        raise InvalidFileTypeError(
            f"File extension '{ext}' does not match content type '{content_type}'"
        )
    
    return content, filename, content_type

