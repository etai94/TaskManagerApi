# tests/test_tasks.py
"""
Tests for task management endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.config import settings
from .test_auth import setup_db, override_get_db  # Reuse auth test fixtures

client = TestClient(app)


def get_api_url(path: str) -> str:
    """Get full API URL for given path"""
    return f"{settings.API_V1_STR}{path}"


#  helper function to create a test user and get token
def create_test_user(username: str, password: str = "TestPass123"):
    """Helper function to create a test user and return token"""
    # Register user
    register_response = client.post(
        get_api_url("/register"),
        json={
            "username": username,
            "password": password
        }
    )
    assert register_response.status_code == 200

    # Login to get token
    login_response = client.post(
        get_api_url("/login"),
        data={
            "username": username,
            "password": password,
            "grant_type": "password"
        }
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"]


#  helper function to create a task
def create_test_task(token: str, description: str = "Test task"):
    """Helper function to create a test task and return its data"""
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        get_api_url("/tasks"),
        json={"description": description},
        headers=headers
    )
    assert response.status_code == 200
    return response.json()



def test_create_task(setup_db):
    """Test creating a new task"""
    #  register and login a user

    token = create_test_user("create_task_user")

    # Create a task
    headers = {"Authorization": f"Bearer {token}"}
    task_data = {"description": "Test task"}
    response = client.post(
        get_api_url("/tasks"),
        json=task_data,
        headers=headers
    )

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test task"
    assert data["completed"] is False
    assert "id" in data
    assert "user_id" in data


def test_create_task_unauthorized():
    """Test creating a task without authentication"""
    task_data = {"description": "Test task"}
    response = client.post(
        get_api_url("/tasks"),
        json=task_data
    )
    assert response.status_code == 401
    assert "detail" in response.json()


def test_create_task_empty_description():
    """Test creating a task with empty description"""
    #  register and login a test user
    token =create_test_user("create_task_empty_description_user")

    # Try to create a task with empty description
    headers = {"Authorization": f"Bearer {token}"}
    task_data = {"description": ""}
    response = client.post(
        get_api_url("/tasks"),
        json=task_data,
        headers=headers
    )

    # Verify response
    assert response.status_code == 422  # Validation error


#  test for updating task description
def test_update_task_description(setup_db):
    """Test updating only the task description"""
    token = create_test_user("update_desc_user")
    task = create_test_task(token, "Original description")

    # Update task description
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(
        get_api_url(f"/tasks/{task['id']}"),
        json={"description": "Updated description"},
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated description"
    assert data["completed"] == False  # Should remain unchanged
    assert data["id"] == task["id"]


# test for updating task completion status
def test_update_task_completion(setup_db):
    """Test updating only the task completion status"""
    token = create_test_user("update_status_user")
    task = create_test_task(token)

    # Update task completion status
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(
        get_api_url(f"/tasks/{task['id']}"),
        json={"completed": True},
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] == True
    assert data["description"] == task["description"]  # Should remain unchanged


#  test for updating both fields
def test_update_task_both_fields(setup_db):
    """Test updating both description and completion status"""
    token = create_test_user("update_both_user")
    task = create_test_task(token)

    # Update both fields
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(
        get_api_url(f"/tasks/{task['id']}"),
        json={
            "description": "New description",
            "completed": True
        },
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "New description"
    assert data["completed"] == True


#  test for non-existent task
def test_update_nonexistent_task(setup_db):
    """Test updating a task that doesn't exist"""
    token = create_test_user("nonexistent_user")

    # Try to update non-existent task
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(
        get_api_url("/tasks/99999"),  # Non-existent task ID
        json={"description": "New description"},
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task does not exist"


#  test for unauthorized task access
def test_update_unauthorized_task(setup_db):
    """Test updating a task owned by another user"""
    # Create first user and their task
    token1 = create_test_user("user1")
    task = create_test_task(token1)

    # Create second user and try to update first user's task
    token2 = create_test_user("user2")
    headers = {"Authorization": f"Bearer {token2}"}
    response = client.put(
        get_api_url(f"/tasks/{task['id']}"),
        json={"description": "Unauthorized update"},
        headers=headers
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You don't have permission to access this task"


def test_delete_task(setup_db):
    """Test successfully deleting a task"""
    # Create user and task
    token = create_test_user("delete_user")
    task = create_test_task(token)

    # Delete the task
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(
        get_api_url(f"/tasks/{task['id']}"),
        headers=headers
    )

    # Verify deletion response matches spec exactly
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}

    # Verify task is actually deleted
    get_response = client.get(
        get_api_url("/tasks"),
        headers=headers
    )
    tasks = get_response.json()
    assert len(tasks) == 0


def test_delete_nonexistent_task(setup_db):
    """Test deleting a task that doesn't exist"""
    token = create_test_user("nonexistent_delete_user")

    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(
        get_api_url("/tasks/99999"),
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task does not exist"


def test_delete_unauthorized_task(setup_db):
    """Test deleting a task owned by another user"""
    # Create first user and their task
    token1 = create_test_user("user1_delete")
    task = create_test_task(token1)

    # Create second user and try to delete first user's task
    token2 = create_test_user("user2_delete")
    headers = {"Authorization": f"Bearer {token2}"}
    response = client.delete(
        get_api_url(f"/tasks/{task['id']}"),
        headers=headers
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "You don't have permission to access this task"

    # Verify task still exists for original user
    headers1 = {"Authorization": f"Bearer {token1}"}
    get_response = client.get(
        get_api_url("/tasks"),
        headers=headers1
    )
    tasks = get_response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task["id"]

