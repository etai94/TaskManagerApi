# TaskManagerApi - Task Management System

A task management system built with FastAPI, SQLAlchemy, and SQLite. The system provides a secure REST API for managing simple personal tasks with user authentication.

## Features

- User registration and authentication using JWT tokens
- Complete CRUD operations for tasks
- Secure API endpoints with OAuth2 authentication
- SQLite database for data persistence
- Comprehensive error handling and input validation
- Optional task filtering by completion status
- Detailed API documentation with Swagger UI

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/task-management-system.git
cd task-management-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root with the following content:
```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

To generate a secure random secret key, use:
```bash
openssl rand -hex 32
```

## Running the Application

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://127.0.0.1:8000/api/v1/docs
- ReDoc: http://127.0.0.1:8000/api/v1/redoc

## API Endpoints

### Authentication
- `POST /api/v1/register` - Register a new user
- `POST /api/v1/login` - Login and receive access token

### Tasks
- `GET /api/v1/tasks` - List all tasks (authenticated)
- `POST /api/v1/tasks` - Create a new task (authenticated)
- `PUT /api/v1/tasks/{task_id}` - Update a task (authenticated)
- `DELETE /api/v1/tasks/{task_id}` - Delete a task (authenticated)

## Running Tests

The project includes comprehensive tests for all endpoints. To run the tests:

```bash
pytest
```

For detailed test output:
```bash
pytest -v
```

## Security Features

- Password hashing using bcrypt
- JWT token authentication
- Token expiration
- Route protection
- Input validation
- SQL injection protection through SQLAlchemy

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   └── tasks.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── models/
│   │   └── base.py
│   └── schemas/
├── tests/
├── requirements.txt
└── README.md
```

## Error Handling

The API includes comprehensive error handling for:
- Invalid credentials
- Unauthorized access
- Non-existent resources
- Input validation
- Database errors

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
