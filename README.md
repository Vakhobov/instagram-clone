# Instagram Clone API

A backend-focused Instagram Clone project built using Django, Django REST Framework, FastAPI, and PostgreSQL.

This project demonstrates REST API development, authentication systems, database design, and scalable backend architecture.

---

## 🚀 Tech Stack

- Python
- Django
- Django REST Framework (DRF)
- PostgreSQL
- SQLite (for development)
- JWT / Token Authentication
- Git & GitHub

---

## ⚙️ Features

- User registration & authentication
- Email verification system
- JWT / Token-based authentication
- Create, update, delete posts
- Pagination
- Custom utilities and shared modules
- Clean architecture structure
- RESTful API endpoints

---

## 📂 Project Structure
- instagram_clone/
- │
- ├── users/ # User management & authentication
- ├── post/ # Post CRUD functionality
- ├── shared/ # Utilities & custom pagination
- ├── templates/ # Email templates
- ├── manage.py
- └── requirements.txt

---

## 🛠 Installation

1️⃣ Clone repository:
  ```bash
  git clone https://github.com/Vakhobov/instagram-clone.git
  cd instagram-clone
  ```
2️⃣ Create virtual environment:
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```
3️⃣ Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
4️⃣ Run migrations:
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
5️⃣ Run server:
  ```bash
  python manage.py runserver
  ```


---

## 📌 API Endpoints (Example)

- `/api/users/register/`
- `/api/users/login/`
- `/api/posts/`
- `/api/posts/<id>/`

---

## 🎯 Purpose

This project was built as a backend development practice project to strengthen knowledge in:

- REST API development
- Database schema design
- Authentication & authorization
- Backend architecture
- Performance optimization

---

## 👨‍💻 Author

Bahrom Vakhobov  
Backend Developer  
GitHub: https://github.com/Vakhobov



