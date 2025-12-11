"""
Custom Exceptions for Business Logic Errors
These exceptions are mapped to appropriate HTTP status codes.
"""
from typing import Optional


class BusinessException(Exception):
    """Base class for business logic errors (4xx)"""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        super().__init__(self.message)


class ValidationError(BusinessException):
    """Validation error (400)"""
    pass


class AuthenticationError(BusinessException):
    """Authentication error (401)"""
    pass


class AuthorizationError(BusinessException):
    """Authorization error (403)"""
    pass


class NotFoundError(BusinessException):
    """Resource not found (404)"""
    pass


class ConflictError(BusinessException):
    """Resource conflict (409)"""
    pass


class RateLimitError(BusinessException):
    """Rate limit exceeded (429)"""
    pass


class ChatMessageTooLongError(BusinessException):
    """Chat message exceeds maximum length (413)"""
    pass


class InvalidFileTypeError(BusinessException):
    """Invalid file type uploaded (415)"""
    pass


class FileTooLargeError(BusinessException):
    """File exceeds maximum size (413)"""
    pass

