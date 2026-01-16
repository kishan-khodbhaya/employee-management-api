
```markdown
# 📘 Employee Management System (EMS)

![Python 3.12](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=flat-square&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production--Ready-success?style=flat-square)

A high-performance, asynchronous RESTful API designed to manage organizational hierarchies and employee lifecycles. Unlike standard CRUD applications, this system implements enterprise-grade patterns including strict Role-Based Access Control (RBAC) and non-blocking I/O.

## 🚀 Key Features

* **Async-First Architecture:** Fully non-blocking database operations using SQLAlchemy Async and FastAPI.
* **Strict RBAC:** Granular middleware-level permission enforcement for **Admin** and **User** roles.
* **Data Integrity:** Robust schema validation via Pydantic and database-level unique constraints.
* **Secure Auth:** Stateless JWT authentication with Bcrypt password hashing.

## 🛠️ Tech Stack

* **Framework:** FastAPI (ASGI)
* **Database:** PostgreSQL with SQLAlchemy 2.0 (Async Engine)
* **Migrations:** Alembic
* **Testing:** Pytest (AsyncIO)

## 📂 Project Structure

```text
emp/
├── 📂 alembic/               # Database migration scripts
│   └── versions/
├── 📂 app/
│   ├── 📂 api/
│   │   └── 📂 routes/      # Auth & Employee endpoints
│   ├── 📂 core/
│   │   ├── 🐍 config.py    # Environment variables
│   │   ├── 🐍 database.py  # Async DB engine
│   │   └── 🐍 security.py  # JWT & Hashing logic
│   ├── 📂 models/          # SQLAlchemy Database Models
│   ├── 📂 schemas/         # Pydantic Response/Request Schemas
│   └── 🐍 main.py          # Application Entry Point
├── 📄 requirements.txt       # Dependency manifest
└── ⚙️ .env.example           # Environment variables template

```

## ⚡ Quick Start

### 1. Prerequisities

Ensure you have Python 3.12+ and PostgreSQL installed.

### 2. Installation

```bash
# Clone repository
git clone [https://github.com/yourusername/ems.git](https://github.com/yourusername/ems.git)
cd ems

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

### 3. Configuration

Rename `.env.example` to `.env` and configure your database credentials and secret keys.

### 4. Database Setup

Apply migrations to create the schema:

```bash
alembic upgrade head

```

### 5. Run Server

```bash
uvicorn app.main:app --reload

```

The API will be available at `http://127.0.0.1:8000`.
👉 **Interactive Swagger UI:** Visit `http://127.0.0.1:8000/docs` to test endpoints directly.

## 📖 API Documentation

Once the server is running, the following documentation endpoints are automatically generated:

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

## 🧪 Testing

The project maintains 90%+ test coverage using an automated async test suite.

```bash
pytest -v --disable-warnings

```

## 🔒 Security

* **Admins:** Full CRUD access to all endpoints.
* **Users:** Read-only access to employee data; strictly prohibited from `POST`, `PUT`, or `DELETE` operations on employee records.

```

```
