from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

import models
from dependencies import get_db, get_current_user

router = APIRouter(prefix="/billing", tags=["Billing"])


# Upgrade user to PRO plan
@router.post("/upgrade")
def upgrade_plan(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    # Create subscription record
    subscription = models.Subscription(
        user_id=current_user.id,
        stripe_customer_id="demo_customer",
        stripe_subscription_id="demo_subscription",
        plan="pro",
        status="active",
        current_period_end=datetime.utcnow() + timedelta(days=30)
    )

    db.add(subscription)

    # Update user plan
    current_user.plan = "pro"

    db.commit()

    return {
        "message": "User upgraded to PRO plan",
        "plan": "pro"
    }

@router.get("/my-subscription")
def get_my_subscription(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    subscription = db.query(models.Subscription).filter(
        models.Subscription.user_id == current_user.id
    ).first()

    if not subscription:
        return {
            "plan": "free",
            "status": "none"
        }

    return {
        "plan": subscription.plan,
        "status": subscription.status,
        "expires": subscription.current_period_end
    }