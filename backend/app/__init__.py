from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
)

load_dotenv()  # ⬅️ Load from .env

db = SQLAlchemy()# db.Model is the base class that all your ORM tables inherit from when you use Flask-SQLAlchemy 
jwt = JWTManager() 

# frontend_url = "http://localhost:8081" #<-- Change this port
allowed_origins = [
    "http://localhost:8081",           # Your local React/Frontend
    "https://salespath-web.web.app"    # Your deployed Firebase/Frontend
]

def create_app():
    app = Flask(__name__)
    app.debug = True

    # ✅ Your MySQL config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("POSTGRES_TOUCH_URL")
    app.config['POSTGRES_DATABASE_URI'] = os.getenv("POSTGRES_CHALUCK_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Bind each DB manually
    app.config['SQLALCHEMY_BINDS'] = {
        'touchdb': os.getenv("POSTGRES_TOUCH_URL"),
        'chaluck': os.getenv("POSTGRES_CHALUCK_URL"),
    }
    # --- JWT Configuration ---
    # You should use a strong, random secret key in a production environment
    # For example, generate with: import secrets; secrets.token_hex(32)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-jwt-key")

    # **THIS IS WHERE YOU SET THE JWT ACCESS TOKEN EXPIRATION TIME**
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes = 15)
    CORS(app, origins=[allowed_origins])   # 🔌 Initialize DB
    db.init_app(app)

    jwt.init_app(app)

    # 🔗 Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
