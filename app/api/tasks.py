# app/api/tasks.py
"""
Task management endpoints for CRUD operations.
"""
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.utils.security import get_current_user
from app.db.models.task import Task
from app.db.models.user import User
from app.api.schemas.task import TaskCreate, TaskUpdate, Task as TaskSchema

# Create router instance
router = APIRouter()


# Create task endpoint
@router.post("/tasks", response_model=TaskSchema)
def create_task(
        *,
        db: Session = Depends(get_db),
        task_in: TaskCreate,
        current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create a new task for the current user.

    Args:
        db: Database session
        task_in: Task creation data
        current_user: Authenticated user

    Returns:
        Created task
    """
    # Create new task object associated with current user
    task = Task(
        description=task_in.description,
        user_id=current_user.id,
        completed=False
    )
    # Add to database
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.get("/tasks", response_model=List[TaskSchema])
def get_tasks(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        completed: bool | None = None
) -> Any:
    """
    Retrieve all tasks for the current user.

    Args:
        db: Database session
        current_user: Authenticated user
        completed: Optional filter by completion status

    Returns:
        List of tasks
    """
    # Build query for current user's tasks
    query = db.query(Task).filter(Task.user_id == current_user.id) #

    # Apply completion status filter if provided
    if completed is not None:
        query = query.filter(Task.completed == completed)

    # Execute query and return results
    return query.all()

# endpoint for updating tasks
@router.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task(
        *,
        db: Session = Depends(get_db),
        task_id: int,
        task_in: TaskUpdate,
        current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update a task.

    Args:
        db: Database session
        task_id: ID of task to update
        task_in: Task update data
        current_user: Authenticated user

    Returns:
        Updated task

    Raises:
        HTTPException: If task not found or not owned by user
    """
    # get task and verify existence + ownership
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task does not exist"
        )
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this task"
        )

    # Update task fields if provided in input
    if task_in.description is not None:
        task.description = task_in.description
    if task_in.completed is not None:
        task.completed = task_in.completed

    # Save changes
    db.add(task)
    db.commit()
    db.refresh(task)

    return task

#  DELETE endpoint
@router.delete("/tasks/{task_id}")
def delete_task(
        *,
        db: Session = Depends(get_db),
        task_id: int,
        current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete a task.

    Args:
        db: Database session
        task_id: ID of task to delete
        current_user: Authenticated user

    Returns:
        Success message

    Raises:
        HTTPException: If task not found or not owned by user
    """
    # find task and verify existence and ownership
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task does not exist"
        )
    if task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this task"
        )

    # delete task
    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}