# 📱 Fullstack App: Expo React Native + Flask + MySQL

This is a fullstack mobile application that combines:

- **Expo React Native** for the frontend (iOS/Android)
- **Flask** (Python microframework) for the backend API
- **MySQL** for persistent data storage

---

## 📁 Project Structure

```
my-fullstack-project/
├── SalesPathNative/         # Expo React Native frontend
├── backend/        # Flask backend with SQLAlchemy
│   ├── app/        # Routes and app logic
│   ├── run.py      # Entry point
│   └── .env        # (NOT COMMITTED) contains DB credentials
├── README.md
└── .gitignore
```

---

## ⚙️ Technologies Used

**Frontend (Mobile)**:
- Expo (React Native)
- TypeScript
- Axios or Fetch API
- React Navigation

**Backend:**
- Flask
- Flask SQLAlchemy
- PyMySQL
- MySQL database
- flask-cors

---

## 🚀 Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

---

### 2. Setup the Backend (Flask)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # (Use venv\Scripts\activate on Windows)
pip install -r requirements.txt
python run.py
```
> It will run on `http://<yourIP>:5000/` (check terminal)

---

### 3. Setup the Frontend (Expo)
```bash
cd SalesPathNative
npm install
npm start  # or 'expo start'
```
> Make sure your Flask API is accessible from mobile devices — use LAN IP (e.g., `192.168.x.x:5000`) in `app.json`:
```json
"extra": {
  "API_URL": "http://192.168.1.10:5000"
}
```

---

## 🌍 Deployment

- Deploy backend to Railway, Render, or self-hosted server (e.g., Synology NAS)
- For Expo frontend, use Expo Go for testing or build standalone apps using EAS
- Store secrets in `.env` and `app.json` securely
- Enable CORS in Flask to allow mobile access

---

## 🔐 Security

- Do **not** commit credentials or `.env` files
- Add `.env`, `venv/`, `node_modules/`, etc. to `.gitignore`
- Rotate credentials if GitHub flags exposure

---

## 🧠 Future Improvements

- JWT-based authentication
- Push notifications (Expo + Firebase)
- Advanced filtering and search
- API docs using Swagger or Postman
- Dockerization for backend

---

## 📬 Contact

If you have questions or want to contribute, feel free to open an issue or pull request.

---

© 2025 Your Name – All rights reserved

