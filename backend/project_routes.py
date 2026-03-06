from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from models import Project
from dependencies import get_db, get_current_user

router = APIRouter()

# Create project
@router.post("/projects")
def create_project(
    name: str,
    description: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    # Check free plan limit
    if current_user.plan == "free":

        project_count = db.query(Project).filter(
            Project.owner_id == current_user.id
        ).count()

        if project_count >= 3:
            raise HTTPException(
                status_code=403,
                detail="Free plan allows only 3 projects. Upgrade to Pro."
            )

    new_project = Project(
        name=name,
        description=description,
        owner_id=current_user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


# Get all projects for logged user
@router.get("/projects")
def get_projects(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    projects = db.query(models.Project).filter(
        models.Project.owner_id == current_user.id
    ).all()

    return projects

@router.put("/projects/{project_id}")
def update_project(
    project_id: int,
    name: str,
    description: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    project.name = name
    project.description = description

    db.commit()
    db.refresh(project)

    return project

@router.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(project)
    db.commit()

    return {"message": "Project deleted successfully"}