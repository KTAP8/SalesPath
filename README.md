# 🧪 Fullstack App: Next.js + Flask + MySQL

This is a fullstack web application that combines:

- Next.js (React framework) for the frontend
- Flask (Python microframework) for the backend API
- MySQL for persistent data storage

---

## 📁 Project Structure

my-fullstack-project/
├── frontend/      # Next.js frontend (TypeScript)
├── backend/       # Flask backend with SQLAlchemy
│   ├── app/       # Routes and app logic
│   ├── run.py     # Entry point
│   └── .env       # (NOT COMMITTED) contains DB credentials
├── README.md
└── .gitignore

---

## ⚙️ Technologies Used

Frontend:
- Next.js
- TypeScript
- React Hooks (useEffect, useState)
- Tailwind CSS (optional)

Backend:
- Flask
- Flask SQLAlchemy
- PyMySQL
- MySQL database

---

## 🚀 Getting Started

### 1. Clone the Repo

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

---

### 2. Setup the Backend (Flask)

cd backend
python -m venv venv
source venv/bin/activate  # (Use venv\Scripts\activate on Windows)
pip install -r requirements.txt

Start the backend server:

python run.py

> It will run on http://<yourIP>:5000/ --> look in terminal when running

---

### 3. Setup the Frontend (Next.js)

cd frontend
npm install
npm run dev

> It will run on http://localhost:3000/

Frontend will fetch from the backend via API:

fetch(`http://<yourIP>:5000//api/hello`) -> same as in backend

---

## 🌍 Deployment

- Deploy frontend to Vercel or Netlify.
- Deploy backend to Railway, Render, or your own server (e.g., Synology NAS).
- Store secrets using .env files or GitHub Secrets.
- Don’t forget to update CORS settings if frontend and backend are on different domains.

---

## 🔐 Security

- Secrets and credentials should never be committed.
- `.env`, `venv/`, `node_modules/`, etc. are excluded via `.gitignore`.
- GitHub will warn you if secrets are exposed — rotate immediately.

---

## 🧠 Future Improvements

- JWT-based authentication
- Production-ready database config
- Dockerization with `docker-compose`
- API docs using Swagger or Postman

---

## 📬 Contact

If you have questions or want to contribute, feel free to open an issue or pull request.

---

© 2025 Your Name – All rights reserved
