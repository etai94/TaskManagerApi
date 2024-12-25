# app/api/schemas/token.py
"""
Token schemas for authentication and authorization.
Defines the structure of token-related data for request/response validation.
"""
from typing import Optional
from pydantic import BaseModel, validator


class Token(BaseModel):
    """
    Schema for token response following OAuth2 spec.

    Attributes:
        access_token (str): The JWT access token
        token_type (str): The token type (always "bearer")
    """
    access_token: str
    token_type: str

    @validator("token_type")
    def validate_token_type(cls, v):
        """Ensure token type is 'bearer'."""
        if v.lower() != "bearer":
            raise ValueError("Token type must be 'bearer'")
        return v.lower()


class TokenData(BaseModel):
    """
    Schema for decoded token data.

    Attributes:
        username (str, optional): Username from token
    """
    username: Optional[str] = None

    @validator("username")
    def username_must_exist(cls, v):
        """Ensure username is not empty if provided."""
        if v is not None and not v.strip():
            raise ValueError("Username cannot be empty")
        return v