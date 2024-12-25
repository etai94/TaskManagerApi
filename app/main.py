# app/main.py
"""
Main application module.
Creates and configures the FastAPI application.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.db.base import init_database
# import routers
from app.api import auth, tasks
from app.core.exceptions import APIException
from app.utils.logging import logger


# Create FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    # openapi_url=f"{settings.API_V1_STR}/openapi.json"
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
    # openapi_url="/openapi.json"
)


#  exception handler for APIException
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """
    Global exception handler for our custom APIException class.
    Converts APIException to a consistent JSON response format.
    """
    # Log the error
    logger.error(
        f"API Error: {exc.message} - Path: {request.url.path}",
        extra={
            "status_code": exc.status_code,
            "detail": exc.detail,
            "path": request.url.path,
            "method": request.method,
        }
    )

    # Prepare error response
    error_response = {
        "detail": exc.message
    }
    #  add additional details if available
    if exc.detail:
        error_response["additional_info"] = exc.detail

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )


# init db on startup
@app.on_event("startup")
async def startup_event():
    """Initialize application"""
    init_database()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register the routers
app.include_router(
    auth.router,
    prefix=settings.API_V1_STR,
    tags=["Authentication"],
    responses={401: {"description": "Authentication failed"}},
)
app.include_router(
    tasks.router,
    prefix=settings.API_V1_STR,
    tags=["Tasks"],
    responses = {
        401: {"description": "Authentication required"},
        403: {"description": "Permission denied"},
        404: {"description": "Task not found"}
    }
)


""""Welcome endpoint"""
@app.get("/")
async def root():
    return {
        "message": "Welcome to Task Management System API",
        "docs": f"{settings.API_V1_STR}/docs",
        "redoc": f"{settings.API_V1_STR}/redoc"
    }