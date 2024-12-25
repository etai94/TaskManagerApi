# app/db/models/user.py
"""
User database model.
Defines the structure of the users table in the database.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from passlib.context import CryptContext
from app.db.base_class import Base
from app.utils.logging import logger

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """
    User model for storing user information and authentication details.

    Attributes:
        __tablename__ = the name of the DB table that will contain this object/s
        id (int): Primary key
        username (str): Unique username
        hashed_password (str): Bcrypt hashed password
        tasks (relationship): Relationship to associated Task objects
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        if 'password' in kwargs:
            password = kwargs.pop('password')
            if not password:
                raise ValueError("Password cannot be empty")
        # If password is provided, hash it before storing
        try:
            if 'password' in kwargs:
                kwargs['hashed_password'] = pwd_context.hash(password)
        except Exception as e:
            logger.error(f"Password hashing error: {str(e)}")
            raise ValueError(f"Error hashing password: {str(e)}")
        super().__init__(**kwargs)