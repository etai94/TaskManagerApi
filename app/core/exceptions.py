# app/core/exceptions.py
"""
Custom exception classes to handle different types of errors.
"""
from fastapi import status
from typing import Optional


class APIException(Exception):
    """Base exception class for all custom API exceptions."""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, detail: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.message)


class AuthenticationError(APIException):
    """Raised when authentication fails."""
    def __init__(self, message: str = "Authentication failed", detail: Optional[str] = None):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class NotFoundError(APIException):
    """Raised when a requested resource is not found."""
    def __init__(self, message: str = "Resource not found", detail: Optional[str] = None):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class PermissionError(APIException):
    """Raised when user doesn't have permission to access a resource."""
    def __init__(self, message: str = "Permission denied", detail: Optional[str] = None):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class ValidationError(APIException):
    """Raised when input validation fails."""
    def __init__(self, message: str = "Validation error", detail: Optional[str] = None):
        super().__init__(message=message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class DuplicateError(APIException):
    """Raised when trying to create a resource that already exists."""
    def __init__(self, message: str = "Resource already exists", detail: Optional[str] = None):
        super().__init__(message=message, status_code=status.HTTP_409_CONFLICT, detail=detail)