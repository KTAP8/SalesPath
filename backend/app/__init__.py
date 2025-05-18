from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()  # ⬅️ Load from .env

db = SQLAlchemy()
jwt = JWTManager()  # ✅ Declare it here


def create_app():
    app = Flask(__name__)
    app.debug = True

    # 🔐 JWT setup
    app.config['JWT_SECRET_KEY'] = os.getenv(
        "JWT_SECRET_KEY")  # use env var in production
    jwt.init_app(app)  # ✅ Initialize JWT manager

    # ✅ Your MySQL config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['POSTGRES_DATABASE_URI'] = os.getenv("POSTGRES_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Bind each DB manually
    app.config['SQLALCHEMY_BINDS'] = {
        'mysql': os.getenv("DATABASE_URL"),
        'postgres': os.getenv("POSTGRES_URL"),
    }

    CORS(app)  # ⬅️ Add this line
    # 🔌 Initialize DB
    db.init_app(app)

    # 🔗 Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
