# 💡 Rate Idea API

A full-featured backend API for managing and rating business ideas — built with **FastAPI**, **MongoDB**, and **JWT**. Users can register, authenticate, post ideas, and manage their own content securely.

---

## 🚀 Features

### 🔐 Authentication
- User registration and login with JWT-based access/refresh tokens
- Secure password hashing using `pbkdf2_sha256`
- Protected routes using FastAPI’s dependency injection
- `/refresh` endpoint to generate a new access token

### 💡 Idea Management
- Create and list startup ideas
- Retrieve your own ideas
- Update or delete your own ideas
- Optional metadata: tags, rating, description

---

## 🧰 Tech Stack

- **FastAPI** – High-performance API framework
- **MongoDB** – NoSQL database
- **PyJWT / jose** – JWT token handling
- **Pydantic** – Data validation
- **Passlib** – Secure password hashing
- **Uvicorn** – ASGI server

---

## 🗂️ Project Structure

```
.
├── app/
│   ├── core/            # Auth utils & settings (JWT, hashing, env)
│   ├── crud/            # DB logic for user operations
│   ├── db/              # MongoDB connection
│   ├── models/          # Pydantic models
│   ├── routes/          # API endpoints (auth + ideas)
│   ├── schemas/         # Pydantic schemas (if used separately)
│   ├── __pycache__/     # Python cache files
│   └── main.py          # FastAPI app entry point
├── .env                 # Secrets and config variables
├── .gitignore           # Git ignore file
├── requirements.txt     # Project dependencies
├── venv/                # Virtual environment
└── .git/                # Git configuration
```

---

## 📦 API Endpoints

### 🔐 Auth Routes

| Method | Route          | Description                     |
|--------|----------------|---------------------------------|
| POST   | `/register`    | Create new user account         |
| POST   | `/login`       | Login with email & password     |
| POST   | `/refresh`     | Get new access token            |
| GET    | `/me`          | Get current authenticated user  |

### 💡 Idea Routes (Protected)

| Method | Route               | Description                       |
|--------|---------------------|-----------------------------------|
| POST   | `/ideas`            | Create a new idea                 |
| GET    | `/ideas`            | List all ideas                    |
| GET    | `/ideas/me`         | Get current user’s ideas          |
| PATCH  | `/ideas/{id}`       | Update idea (if owner)            |
| DELETE | `/ideas/{id}`       | Delete idea (if owner)            |

---

## 🛠️ Setup & Run Locally

### 1. Clone the Repo
```
git clone https://github.com/Marwankishkk/idea-review-api.git
cd idea-review-api

```

### 2. Create `.env` File
```
# .env

MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=idea_vault
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Run the Server
```
uvicorn app.main:app --reload
```

---

## 🔐 Example Auth Flow

### 1. Register a User
```http
POST /register
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

### 2. Login
```http
POST /login
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

Returns:
```json
{
  "access_token": "abc...",
  "refresh_token": "xyz...",
  "token_type": "bearer"
}
```

### 3. Use Token for Protected Routes
Add this header to all `/ideas/*` requests:
```
Authorization: Bearer <access_token>
```

---


