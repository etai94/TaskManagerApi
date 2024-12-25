# Task Management System

A robust task management system built with FastAPI, SQLAlchemy, and SQLite. The system provides a secure REST API for managing personal tasks with user authentication.

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [API Usage Examples](#api-usage-examples)
7. [Running Tests](#running-tests)
8. [Security Features](#security-features)
9. [Project Structure And Architecture](#project-structure-and-architecture)
10. [Data Management](#data-management)
11. [Error Handling](#error-handling)
12. [Future Enhancements and Roadmap](#future-enhancements-and-roadmap)

## Features

- User registration and authentication using JWT tokens
- Complete CRUD operations for tasks
- Secure API endpoints with OAuth2 authentication
- SQLite database for data persistence
- Comprehensive error handling and input validation
- Optional task filtering by completion status
- Detailed API documentation with Swagger UI
- "test" and "production" modes, can be changed

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Set up the project:
```bash
# Clone the repository
git clone https://github.com/etai94/TaskManagerApi.git
# Navigate to the backend directory
cd TaskManagerApi/backend
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate    # On Windows
source venv/bin/activate # On Unix or MacOS
# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root with the following content:
```env
SECRET_KEY=YOUR_KEY_HERE
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
To generate a secure random secret key, use in cmd:
bash:
python -c "import secrets; print(secrets.token_hex(32))"

replace the output with YOUR_KEY_HERE .


## Running the Application

Start the server using one of these methods:

1. Using Python module path (recommended for command line):
```bash
# Make sure you're in the backend directory and your venv is activated
python -m uvicorn app.main:app --reload
```

After the server is running, you can access each of the API documentation:
- Swagger UI: http://127.0.0.1:8000/api/v1/docs
- ReDoc: http://127.0.0.1:8000/api/v1/redoc

##  Pycharm setup: 
  - Open project directory as a project.
  - In the terminal write "pip install -r requirements.txt"
  - Click on the arrow near the right "RUN" triangle to open a drop down menu -> edit configurations...
  - The run configuration window will open. Make a new configuration and select "FastAPI" configuration. After creating the new configuration, fill like in the image:
![תמונה](https://github.com/user-attachments/assets/67a0e8e4-f67d-47d0-81dd-bee095bd31a5)
  - You can run after this. To run tests you have the server running.

## API Usage Examples

### User Registration

Windows CMD:
```bash
curl -X POST http://localhost:8000/api/v1/register -H "Content-Type: application/json" -d "{\"username\": \"testuser\", \"password\": \"TestPass123\"}"
```

PowerShell:
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/v1/register" -Headers @{"Content-Type"="application/json"} -Body '{"username": "testuser", "password": "TestPass123"}'
```

Unix/Linux:
```bash
curl -X POST http://localhost:8000/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "TestPass123"}'
```

### User Login

Windows CMD:
```bash
curl -X POST http://localhost:8000/api/v1/login -H "Content-Type: application/x-www-form-urlencoded" -d "username=testuser&password=TestPass123"
```

PowerShell:
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/v1/login" -Headers @{"Content-Type"="application/x-www-form-urlencoded"} -Body "username=testuser&password=TestPass123"
```

### Create Task

Windows CMD:
```bash
curl -X POST http://localhost:8000/api/v1/tasks -H "Authorization: Bearer YOUR_TOKEN_HERE" -H "Content-Type: application/json" -d "{\"description\": \"Buy groceries\"}"
```

PowerShell:
```powershell
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/v1/tasks" -Headers @{"Authorization"="Bearer YOUR_TOKEN_HERE"; "Content-Type"="application/json"} -Body '{"description": "Buy groceries"}'
```

### Get All Tasks

Windows CMD:
```bash
curl -X GET http://localhost:8000/api/v1/tasks -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

PowerShell:
```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:8000/api/v1/tasks" -Headers @{"Authorization"="Bearer YOUR_TOKEN_HERE"}
```

## Running Tests

The project includes the basic verification tests that were provided with the assignment (test_ver.py), which have been extended with additional test cases to ensure robust functionality. To run these verification tests:

```bash
pytest test_ver.py -v
```

*Note: Throughout the development process, comprehensive tests were written and executed for each component (auth, tasks, security, etc.). These additional tests are not included in the README instructions as they require further adjustments to run collectively.*

## Security Features

- Password hashing using bcrypt (implemented in `app/utils/security.py:get_password_hash()` and `app/db/models/user.py`)
- OAuth2 with JWT token authentication with expiration (implemented in `app/utils/security.py:create_access_token()` and `verify_token()`)
- Token-based route protection (implemented in `app/utils/security.py:get_current_user()`)
- Input validation using Pydantic models (implemented across `app/api/schemas/`)
- SQL injection protection through SQLAlchemy ORM (implemented in `app/db/models/` and database queries)

## Project Structure And Architecture

### Files and Directories Hierarchy Tree
```
backend/
├── app/                  
│   ├── api/                  # API layer 
│   │   ├── auth.py          # Authentication realted endpoints and logic
│   │   ├── tasks.py         # Task related endpoints
│   │   └── schemas/         # Request/Response data models
│   │       ├── task.py      
│   │       ├── token.py     # Authentication token schemas
│   │       └── user.py   
│   │
│   ├── core/                # Core application components
│   │   ├── config.py        # Application configuration
│   │   └── exceptions.py    # Custom exception definitions
│   │
│   ├── db/                  # Database layer
│   │   ├── base.py         # Database initialization, session and utils
│   │   ├── base_class.py   # SQLAlchemy base class
│   │   └── models/         # Database models
│   │       ├── task.py    
│   │       └── user.py    
│   │
│   ├── utils/              # Utility functions
│   │   ├── logging.py      # Logging configuration
│   │   └── security.py     # Security utilities (JWT handling, passwords hasing)
│   │
│   └── main.py             # FastAPI application entry point
│
├── tests/                 
│   ├── test_auth.py        # Authentication tests
│   ├── test_routes.py      # API routes basic tests
│   ├── test_security.py    # Security utilities tests
│   ├── test_tasks.py       # Task operations basic tests
│   ├── test_token.py       # Token verification test
│   └── test_ver.py         # Main verification tests (Run these!)
│
├── .env                     
└── requirements.txt         #  dependencies
```

### Project Architecture

The project follows a layered architecture focused on separation of concerns and modularity:

1. **API Layer** (`app/api/`):
   - Implements REST endpoints for authentication and task management
   - Contains schema definitions for request/response validation
   - Handles HTTP communication and data transformation
   - Provides a clear contract for API consumers through Pydantic schemas

2. **Database Layer** (`app/db/`):
   - Manages data persistence through SQLAlchemy ORM
   - Defines database models and their relationships
   - Handles database session management
   - Provides a clean abstraction for data access

3. **Core Layer** (`app/core/`):
   - Contains fundamental application configuration
   - Defines system-wide settings and constants
   - Manages custom exception definitions

4. **Utilities Layer** (`app/utils/`):
   - Provides cross-cutting functionality used across other layers
   - Implements security services (JWT handling, password management)
   - Configures application-wide logging

The architecture promotes:
- Clear separation of concerns
- Modular design for maintainability
- Cohesive grouping of related functionality
- Loose coupling between layers through well-defined interfaces


## Data Management

- SQLite database with SQLAlchemy ORM for data persistence (implemented in `app/db/base.py`)
- User model with secure password storage and task relationships (implemented in `app/db/models/user.py`)
- Task model with user ownership and completion status (implemented in `app/db/models/task.py`)
- Database session management with connection pooling (managed in `app/db/base.py:get_db()`)
- Data validation with Pydantic models (implemented in `app/api/schemas/`)
- Row-level security ensuring users can only access their own data (implemented in task endpoints)
- Automatic relationship handling between users and tasks (implemented through SQLAlchemy relationships)


## Error Handling (TBD*)

The API includes error handling for:
- Invalid credentials
- Unauthorized access
- Non-existent resources
- Input validation
- Database errors

*Note: The centralization of error handling and exception management is still in progress and was not completed by the deadline. Further improvements are planned(as can be seen in exceptions.py) to implement a more unified error handling system. Meantime, different components in the app return error messages in different ways - but the errors are still handeled.*

## Future Enhancements and Roadmap

### Immediate Priorities
- Complete centralized error handling implementation        (status: implemented, need to refactor most files for it to work. miscalculated the time and tried working on it and start the front simultaneously)
- Adjust and extend the tests and make some stress tests    (status: Following error handling changes, some tests cause problems and need further work for them to work(the tests, not the app )
- Finish the basic frontend UX/UI                              (status: missing some UI componenets and the connectivity between the FE to the BE endpoint still does not work) 
- Add rate limiting for API endpoints  (security)
- Add an easy migration feature
  
### Feature Enhancements
- Add pagination for task listing                     
- Implement comprehensive logging system
- Implement password reset functionality
- Add task categories and labels
- Implement task due dates and reminders
- Add task sharing between users
- Add email verification for new users and enhance auth process
















