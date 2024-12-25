# tests/test_routes.py
from fastapi.testclient import TestClient
from app.main import app
from app.core.exceptions import NotFoundError
from app.core.config import settings

client = TestClient(app)


def test_api_prefix():
    response = client.get("/docs")  # OpenAPI docs should be available
    assert response.status_code == 200
    response = client.get("/")  # Root endpoint should still work
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Task Management System API",
        "docs": f"{settings.API_V1_STR}/docs",
        "redoc": f"{settings.API_V1_STR}/redoc"
    }



#   test for error handler
def test_error_handler():
    """Test custom error handler with a test endpoint"""
    @app.get("/test-error")
    async def test_error():
        raise NotFoundError("Test resource not found", detail="Additional error info")

    response = client.get("/test-error")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Test resource not found"
    assert data["additional_info"] == "Additional error info"