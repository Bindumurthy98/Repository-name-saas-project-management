from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from models import Task

router = APIRouter()

# Create task
@router.post("/tasks")
def create_task(
    title: str,
    description: str,
    project_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_task = Task(
        title=title,
        description=description,
        project_id=project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# Get tasks for a project
@router.get("/tasks/{project_id}")
def get_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tasks = db.query(Task).filter(Task.project_id == project_id).all()

    return tasks