# app/api/auth.py
"""
Authentication endpoints for user registration and login.
"""
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.utils.security import create_access_token, get_password_hash, verify_password
from app.db.base import get_db
from app.db.models.user import User
from app.api.schemas.user import UserCreate, User as UserSchema
from app.api.schemas.token import Token
from app.utils.logging import logger
from app.core.exceptions import AuthenticationError, DuplicateError

router = APIRouter()

@router.post("/register", response_model=UserSchema)
def register_user(
        *,
        db: Session = Depends(get_db),
        user_in: UserCreate,
) -> Any:
    """
    Register a new user.

    Args:
        db: Database session
        user_in: User registration data

    Returns:
        Newly created user

    Raises:
        DuplicateError: If username already exists
    """
    logger.info(f"Attempting to register user: {user_in.username}")
    try:
        # Check if user exists
        user = db.query(User).filter(User.username == user_in.username).first()
        if user:
            logger.warning(f"Registration failed: Username {user_in.username} already exists")
            raise DuplicateError(
                detail="Username already registered"
            )

        # Create new user
        user = User(
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"Successfully registered user: {user_in.username}")
        return user
    except Exception as e:
        logger.error(f"Error during user registration: {str(e)}")
        raise AuthenticationError(
            message="Registration failed",
            detail="An error occurred during registration"
        )




@router.post("/login", response_model=Token)
async def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.

    Args:
        db: Database session
        form_data: OAuth2 form containing username and password

    Returns:
        Access token for authentication

    Raises:
        AuthenticationError: If authentication fails
    """
    logger.info(f"=== Login Attempt Started for {form_data.username} ===")
    try:
        data_username = form_data.username
        data_pwd = form_data.password
        # Authenticate user
        user = db.query(User).filter(User.username == data_username).first()
        if not user or not verify_password(data_pwd, user.hashed_password):
            logger.warning(f"Failed login attempt for user: {form_data.username}")
            raise AuthenticationError(
                message="Login failed",
                detail="Incorrect username or password",
                headers = {"WWW-Authenticate": "Bearer"},
            )
        logger.info(f"User authenticated successfully: {user.username}")
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )

        logger.info("=== Login Attempt Completed ===")
        # return token in OAuth2 format
        return Token(
            access_token=access_token,
            token_type="bearer"
        )
    except AuthenticationError:
        raise
    except Exception as e:
        logger.error(f"=== Login Error ===")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {str(e)}")
        logger.error("=== End Error Details ===")
        raise AuthenticationError(
            message="Login failed",
            detail=f"An error occurred during login. Error type : {type(e).__name__}. Full error message:  {str(e)}."
        )


