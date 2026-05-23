# CourseForces 🚀  
### An Online Course Assessment Platform

CourseForces is a full-stack ed-tech platform that enables professors and students to interact through courses, quizzes, assessments, and analytics. The platform supports multiple user roles, secure authentication, quiz creation, automated evaluation workflows, and course collaboration.

Built using **ReactJS**, **Django**, and **SQLite**, CourseForces provides a smooth and interactive learning experience for both instructors and students.

---

## 🔗 GitHub Repository

https://github.com/vaibhavi-agrawal/CourseForces_CF

---

## ✨ Features

### 👨‍🏫 Professor Features
- Create and manage courses
- Invite students and professors to courses
- Create quizzes with:
  - Single Correct MCQs
  - Multi Correct MCQs
  - Subjective Questions
- Set quiz timings and instructions
- View submissions and marks
- Evaluate student performance

### 👨‍🎓 Student Features
- Join courses through invitations
- Attempt quizzes
- View quiz information and submissions
- Participate in multiple courses with different roles

### 🔐 Authentication & Security
- User registration and login
- Email verification system
- Token-based authentication
- Role-based access control

### 📧 Notifications
- Email invitations for course joining
- Account activation emails

---

## 🛠️ Tech Stack

### Frontend
- ReactJS
- Tachyons CSS
- React Router

### Backend
- Django
- Django REST Framework

### Database
- SQLite

---

## 📂 Project Structure

```bash
projs/
│
├── frontend/          # React Frontend
├── backend/           # Django Backend
├── README.md
└── ...
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/vaibhavi-agrawal/CourseForces_CF.git
cd projs
```

---

## 🚀 Backend Setup (Django)

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Linux / Mac

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py migrate
```

### Start Backend Server

```bash
python manage.py runserver
```

Backend runs on:

```bash
http://127.0.0.1:8000/
```

---

## 💻 Frontend Setup (React)

```bash
cd frontend
npm install
npm start
```

Frontend runs on:

```bash
http://192.168.1.13:4225/
```

---

## 🧠 Core Functionalities

- Course Creation & Management
- Quiz Creation System
- MCQ/MSQ/Subjective Questions
- Email-based Course Invitations
- Authentication System
- Quiz Attempt Tracking
- Marks & Analytics Dashboard
- Multi-role User Support

---

## 🗃️ Database Design

Main Entities:
- MyUser
- Course
- Quiz
- Question
- Option
- QuizAttempt

The system is designed using relational mappings between users, courses, quizzes, and attempts.

---

## 🔥 Unique Highlights

- A user can be:
  - Professor in one course
  - Student in another course

- Dynamic quiz system with multiple question types

- Email-based verification and invitation workflow

- Token-based secure authentication

---

## 📈 Future Improvements

- Real-time quiz monitoring
- Leaderboards
- AI-based performance analytics
- Dark mode UI
- Live notifications
- Deployment using Docker & AWS

---



## 📜 License

This project is for educational purposes.