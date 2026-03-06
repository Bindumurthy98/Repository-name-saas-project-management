# Project Management SaaS

## Overview

This project is a **Project Management SaaS application** built with **FastAPI, MySQL, React, and Stripe**.

It provides a **user panel** for managing projects and subscriptions and an **admin panel** for monitoring users and subscriptions.

The system includes **JWT authentication, role-based access control, Stripe subscription billing, and project limits based on subscription plans**.

---

# Tech Stack

## Backend

* FastAPI
* SQLAlchemy
* MySQL 8
* Alembic migrations
* JWT Authentication
* Stripe API (Subscriptions & Webhooks)

## Frontend

* React (Vite)
* Tailwind CSS
* React Router
* Axios
* Stripe.js

---

# Features

## User Panel

Users can:

* Register and login
* Create and manage projects
* Upgrade to Pro subscription
* View subscription status

### Free Plan

* Maximum **3 projects**

### Pro Plan

* **Unlimited projects**

---

## Admin Panel

Admins can:

* View all users
* View all subscriptions
* Monitor subscription status

Admin routes are protected with **role-based access control**.

---

# Database Models

### User

* id
* email
* hashed_password
* role (user | admin)
* is_active
* stripe_customer_id
* plan
* created_at

### Project

* id
* name
* description
* owner_id
* created_at

### Subscription

* id
* user_id
* stripe_customer_id
* stripe_subscription_id
* plan
* status
* current_period_end
* created_at

---

# Authentication

Authentication is implemented using:

* **JWT access tokens**
* **Password hashing**
* **Protected routes**

Users must login to access project and subscription endpoints.

---

# Stripe Subscription Flow

1. User clicks **Upgrade to Pro**
2. Stripe Checkout Session is created
3. User completes payment
4. Stripe sends a **Webhook**
5. Backend verifies webhook signature
6. Subscription status is updated in the database
7. User plan changes from **Free → Pro**

---

# Backend Setup

### 1. Clone the repository

```
git clone <repository_url>
cd saas-app
```

### 2. Create virtual environment

```
cd backend
python -m venv venv
```

Activate:

Windows

```
venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` file based on `.env.example`.

Example:

```
DATABASE_URL=mysql+pymysql://root:password@localhost/saas_db
SECRET_KEY=your_secret_key
STRIPE_SECRET_KEY=your_stripe_secret
STRIPE_WEBHOOK_SECRET=your_webhook_secret
```

### 5. Run migrations

```
alembic upgrade head
```

### 6. Start backend server

```
uvicorn main:app --reload
```

API Docs:

```
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

### Install dependencies

```
cd frontend
npm install
```

### Run development server

```
npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

# Environment Variables

Example `.env.example`

```
DATABASE_URL=
SECRET_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
```

---

# Project Structure

```
saas-app
│
├── backend
│   ├── models.py
│   ├── routes
│   ├── alembic
│   └── main.py
│
├── frontend
│   ├── src
│   ├── pages
│   └── services
│
├── .env.example
└── README.md
```

---

# Security

* JWT Authentication
* Password hashing
* Stripe webhook signature verification
* Role-based route protection
* Owner-only project access

---

# Future Improvements

* Full UI dashboard
* Payment history
* Team collaboration
* Project analytics
* Production deployment

---

# Author

Project developed as a **Full Stack SaaS Application** using FastAPI, React, and Stripe.
