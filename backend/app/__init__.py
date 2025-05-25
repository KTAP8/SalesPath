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

    # 🔗 Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
