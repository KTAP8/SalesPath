from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager

load_dotenv()  # ⬅️ Load from .env

db = SQLAlchemy()# db.Model is the base class that all your ORM tables inherit from when you use Flask-SQLAlchemy 


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

    CORS(app)  # ⬅️ Add this line
    # 🔌 Initialize DB
    db.init_app(app)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "change_me_now")
    jwt = JWTManager(app) 

    # 🔗 Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
