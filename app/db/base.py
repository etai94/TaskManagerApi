# app/db/base.py
"""
Database configuration module.
Sets up SQLAlchemy and creates the database engine.
"""
import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.utils.logging import logger
from app.db.base_class import Base
from app.db.models.user import User
from app.db.models.task import Task



# Check database path and permissions
db_path = settings.DATABASE_URL.replace('sqlite:///', '')
db_dir = os.path.dirname(db_path) or '.'
# Check directory permissions
try:
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    if not os.access(db_dir, os.W_OK):
        logger.error(f"No write permission in directory {db_dir}")
        # else:
        # logger.info(f"Directory {db_dir} is writable")
except Exception as e:
    logger.error(f"Error checking directory permissions: {e}")

TARGET_DB = settings.DATABASE_URL

# Create SQLAlchemy engine
engine = create_engine(
    TARGET_DB,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=True
)
# Create SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#  Database initialization function
def init_database():
    """
    Initialize database and create all tables.
    Should be called when application starts.
    """
    try:
        logger.info("Starting database initialization...")

        if settings.ENV == "test":
            logger.info("We are in test mode (ENV = test)")
            Base.metadata.drop_all(bind=engine)
        else:
            logger.info("We are in production mode (ENV = production)")
        # logger.info(f"Registered models: {Base.metadata.tables.keys()}")
        # test and log connecting to the database
        with engine.connect() as conn:
            logger.info("Successfully connected to database")

        # create database tables
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise


# dependency
def get_db():
    """
    Get database session.
    Dependencies will use this to get a session.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        # log database errors
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        db.close()

