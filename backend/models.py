from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base
from datetime import datetime
from sqlalchemy import ForeignKey

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="user")  # user | admin
    is_active = Column(Boolean, default=True)
    stripe_customer_id = Column(String(255), nullable=True)
    
    plan = Column(String(50), default="free")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(500))

    owner_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255))
    description = Column(String(500))

    project_id = Column(Integer, ForeignKey("projects.id"))

    created_at = Column(DateTime, default=datetime.utcnow)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    stripe_customer_id = Column(String(255))
    stripe_subscription_id = Column(String(255))

    plan = Column(String(50), default="free")
    status = Column(String(50), default="active")

    current_period_end = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)