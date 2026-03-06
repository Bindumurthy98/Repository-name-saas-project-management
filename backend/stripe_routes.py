import os
import stripe
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from dependencies import get_db, get_current_user
import models

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(prefix="/stripe", tags=["Stripe"])


# Create Stripe Checkout Session
@router.post("/create-checkout-session")
def create_checkout_session(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Pro Plan"
                    },
                    "unit_amount": 1000,  # $10
                    "recurring": {"interval": "month"}
                },
                "quantity": 1
            }],
            success_url="http://localhost:8000/success",
            cancel_url="http://localhost:8000/cancel",
            metadata={
                "user_id": current_user.id
            }
        )

        return {"checkout_url": session.url}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )

    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle event
    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]
        user_id = session["metadata"]["user_id"]

        user = db.query(models.User).filter(models.User.id == user_id).first()

        if user:
            user.plan = "pro"

            subscription = models.Subscription(
                user_id=user.id,
                plan="pro",
                status="active"
            )

            db.add(subscription)
            db.commit()

    return {"status": "success"}