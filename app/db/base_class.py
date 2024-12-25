# app/db/base_class.py
"""
Base class for SQLAlchemy models - different file to avoid a loop
"""
from typing import Any
from sqlalchemy.ext.declarative import declarative_base

# Create the declarative base that will be used by all models
Base = declarative_base()