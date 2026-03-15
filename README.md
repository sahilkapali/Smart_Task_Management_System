# 🚀 Smart Task Management System

A robust, full-stack Task Management application featuring a **Django REST Framework** backend and a **React (Vite)** frontend. This project implements secure JWT authentication and user-specific data isolation.

---

## 📖 Table of Contents
1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Tech Stack](#-tech-stack)
4. [Project Structure](#-project-structure)
5. [Installation & Setup](#-installation--setup)
6. [API Endpoints](#-api-endpoints)
7. [Future Improvements](#-future-improvements)
8. [Conclusion](#-conclusion)

---

## 🌟 Project Overview
The **Smart Task Management System** provides a secure environment for users to organize their daily activities. The "Smart" aspect ensures data integrity and privacy: users can only interact with their own tasks, and the system automatically handles session security via modern web standards.

---

## ✨ Features
- **Secure Auth**: Implementation of JWT (JSON Web Tokens) via SimpleJWT.
- **Session Persistence**: Automated token refreshing via Axios Interceptors.
- **CRUD Operations**: Create, Read, Update, and Delete tasks with instant UI updates.
- **Data Protection**: Backend QuerySet overrides to prevent cross-user data leakage.
- **Modern UI**: Fully responsive design built with React 18 and CSS3.

---

## 🛠 Tech Stack

### **Backend**
- **Framework**: Django 5.1
- **API**: Django REST Framework (DRF)
- **Authentication**: SimpleJWT (Access & Refresh tokens)
- **Database**: SQLite3

### **Frontend**
- **Framework**: React 18 (Vite)
- **State Management**: React Context API
- **HTTP Client**: Axios (with custom Interceptors)
- **Routing**: React Router DOM v6

---

## 📂 Project Structure
```text
Smart_Task_Management_System/
├── backend/
│   └── task_manager/          # Django Project Root
│       ├── tasks/             # Task logic & models
│       ├── users/             # User Auth & JWT logic
│       ├── task_manager/      # Main settings & URLs
│       └── manage.py
├── frontend/
│   └── smart-task-mgmt/       # React Project Root
│       ├── src/
│       │   ├── api/           # Axios Interceptors
│       │   ├── context/       # AuthProvider state
│       │   ├── pages/         # Dashboard, Login, Register
│       │   └── App.jsx        # Routing
│       └── package.json
└── README.md
```

🚀 Installation & Setup

1. Backend Setup
```
   cd backend/task_manager
    python -m venv venv
    # Activate on Windows:
    venv\Scripts\activate
    # Install Dependencies:
    pip install -r requirements.txt
    # Database Migration:
    python manage.py makemigrations
    python manage.py migrate
    # Start Server:
    python manage.py runserver
```
2. Frontend Setup
```
  cd frontend/smart-task-mgmt
  npm install
  npm run dev
```

🔐 API Endpoints
 | Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/users/auth/register/` | Register a new user |
| **POST** | `/api/users/auth/login/` | Login & receive tokens |
| **POST** | `/api/users/auth/token/refresh/` | Refresh expired access token |
| **GET** | `/api/tasks/` | List all tasks for logged-in user |
| **POST** | `/api/tasks/` | Create a new task |
| **DELETE** | `/api/tasks/<id>/` | Remove a task |

🔮 Future Improvements

To move this project from a prototype to a production-ready application, the following features are planned:
- Task Prioritization: Adding "High, Medium, Low" labels to tasks.
- Deadlines: Integration of a calendar view and date-based notifications.
- Dark Mode: A toggleable UI theme for better user accessibility.
- Social Login: Integration of Google/GitHub OAuth for faster onboarding.
- Categorization: Ability to group tasks into "Work," "Personal," or "Study" categories.

🏁 Conclusion

This project demonstrates the power of combining a structured Django backend with a dynamic React frontend. By implementing JWT and custom middleware, the Smart Task Management System ensures that performance and security are prioritized, providing a solid foundation for a scalable productivity tool.

📄 License

MIT License

Copyright (c) 2026 Sahil Kapali

This project is open-source. You are free to use, modify, and distribute it, provided that the original copyright notice and this permission notice are included in all copies or substantial portions of the software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
