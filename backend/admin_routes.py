from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from dependencies import get_db, get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])


# Check if current user is admin
def admin_only(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


# View all users
@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    admin: models.User = Depends(admin_only)
):
    users = db.query(models.User).all()
    return users


# View all subscriptions
@router.get("/subscriptions")
def get_all_subscriptions(
    db: Session = Depends(get_db),
    admin: models.User = Depends(admin_only)
):
    subscriptions = db.query(models.Subscription).all()
    return subscriptions


# View user → subscription mapping
@router.get("/user-subscriptions")
def get_user_subscriptions(
    db: Session = Depends(get_db),
    admin: models.User = Depends(admin_only)
):
    data = db.query(models.User, models.Subscription).join(
        models.Subscription,
        models.User.id == models.Subscription.user_id,
        isouter=True
    ).all()

    result = []

    for user, subscription in data:
        result.append({
            "user_id": user.id,
            "email": user.email,
            "plan": subscription.plan if subscription else "free",
            "status": subscription.status if subscription else "none"
        })

    return result