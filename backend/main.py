from billing_routes import router as billing_router
from admin_routes import router as admin_router
from task_routes import router as task_router
from fastapi import FastAPI
from database import engine, Base
import models
from routes.users import router as user_router
from project_routes import router as project_router
from stripe_routes import router as stripe_router

app = FastAPI()

app.include_router(project_router)

app.include_router(task_router)

Base.metadata.create_all(bind=engine)

app.include_router(user_router)

app.include_router(admin_router)

app.include_router(billing_router)

app.include_router(stripe_router)

@app.get("/")
def root():
    return {"message": "Backend + Database working!"}