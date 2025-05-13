from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()  # ⬅️ Load from .env

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.debug = True

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
