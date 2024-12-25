# app/utils/security.py
"""
Security utilities for JWT token handling, password hashing, and user authentication.
Centralizes all security-related functionality.
"""
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, InvalidSignatureError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.db.base import get_db
from app.utils.logging import logger
from app.api.schemas.token import TokenData
from app.db.models.user import User
from app.core.exceptions import AuthenticationError

# password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login",
    scheme_name="JWT",
    auto_error=True
)

# token type constants
TOKEN_TYPE_ACCESS = "access"




def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token.

    Args:
        data (dict): Data to encode in the token
        expires_delta (Optional[timedelta]): Token expiration time

    Returns:
        str: Encoded JWT token
    Raises:
        ValueError: If token data is empty
    """
    if not data:
        raise ValueError("Token data cannot be empty")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        # add  token type and issued at time
    to_encode.update({
        "exp": expire,
        "type": TOKEN_TYPE_ACCESS,
        "iat": datetime.now(timezone.utc)
    })
    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating token: {str(e)}")
        raise ValueError(f"Error creating token: {str(e)}")


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.

    Args:
        token (str): JWT token to verify

    Returns:
        dict: Decoded token payload

    Raises:
        HTTPException: With standardized error message for any token validation error
            """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iat": True,
            }
        )
        if payload.get("type") != TOKEN_TYPE_ACCESS:
            raise InvalidTokenError("Invalid token type")

        return payload
    except (ExpiredSignatureError, InvalidSignatureError, InvalidTokenError) as e:
        # log specific error but send to the user only the generic "Could not validate credentials"
        logger.error(f"Token validation failed: {str(e)}")
        raise AuthenticationError(detail="Could not validate credentials")
    except Exception as e:
        logger.error(f"Unexpected error during token validation: {str(e)}")
        raise AuthenticationError(detail=f"Could not validate credentials ")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password (str): Password to verify
        hashed_password (str): Hashed password to compare against

    Returns:
        bool: True if password matches, False otherwise
    Raises:
        ValueError: If either password is empty
    """
    if not plain_password or not hashed_password:
        raise ValueError("Passwords cannot be empty")
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification error: {str(e)}")
        return False



def get_password_hash(password: str) -> str:
    """
    Hash a password.

    Args:
        password (str): Password to hash

    Returns:
        str: Hashed password
    Raises:
        ValueError: If password is empty
    """
    if not password:
        raise ValueError("Password cannot be empty")
    return pwd_context.hash(password)


async def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)   # FastAPI will extract the Bearer token
) -> User:
    """
    Get current authenticated user.

    Args:
        db (Session): Database session
        token (str): JWT token from request

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: With standardized error message for any authentication error
    """

    try:
        # Verify the JWT token
        payload = verify_token(token)
        username: str = payload.get("sub")
        if username is None:
            logger.error("Token payload missing username")
            raise AuthenticationError(detail="ERROR : Username is missing")
        # validate token data using the TokenData schema
        token_data = TokenData(username=username)

        # gt user from db
        user = db.query(User).filter(User.username == token_data.username).first()
        if user is None:
            logger.error(f"User not found: {username}")
            raise AuthenticationError(detail=f"ERROR : User not found: {username}")
        return user
    except Exception as e:
        logger.error(f"Unexpected error in authentication: {str(e)}")
        raise AuthenticationError(detail=f"Unexpected error in authentication, check logs for more details")
