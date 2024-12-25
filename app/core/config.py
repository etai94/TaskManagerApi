# app/core/config.py
"""
Application configuration module.
Contains settings and configuration variables for the application.
"""
from pydantic import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # ------ API Settings ------
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Task Management System"
    API_DESCRIPTION: str = """
        Task Management System API - Manage your tasks with a simple REST API.

        ## Features
        * User registration and authentication
        * Create and manage tasks
        * Filter tasks by completion status
        * Secure API with JWT authentication

        ## Authentication
        All task management endpoints require authentication using JWT tokens.
        1. Register a new user using `/register`
        2. Login using `/login` to get your access token
        3. Use the token in the Authorization header: `Bearer your_token_here`
        """


    # ------ Security settings ------
    # Generate using: openssl rand -hex 32
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ------ Environment settings ------
    ENV: str = os.getenv("ENV", "production")  # values: production / test

    # ------ Database settings ------
    # Production database - persistent storage
    SQLITE_URL: str = "sqlite:///./sql_app.db"
    # Test database - temporary storage
    TEST_SQLITE_URL: str = "sqlite:///./test.db"

    @property
    def DATABASE_URL(self) -> str:
        """Returns appropriate database URL based on environment"""
        return self.TEST_SQLITE_URL if self.ENV == "test" else self.SQLITE_URL

    class Config:
        case_sensitive = True


#  global settings object
settings = Settings()
