# SaaS Project Management App

## Tech Stack
Backend
- FastAPI
- SQLAlchemy
- MySQL
- JWT Authentication
- Stripe Subscription API

Frontend
- React (Vite)
- Tailwind CSS
- React Router
- Axios

## Features

User Panel
- Register / Login
- Create and manage projects
- Subscription upgrade via Stripe

Admin Panel
- View users
- View subscriptions
- Monitor system usage

## Business Logic

Free Plan
- Maximum 3 projects

Pro Plan
- Unlimited projects

## Stripe Integration

- Stripe Checkout for subscription
- Webhook handling
- Subscription status sync with database

## Setup

Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Frontend
cd frontend
npm install
npm run dev

## Environment Variables

Create `.env` using `.env.example`.

---

Project built for SaaS architecture demonstration.
