from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # ✅ Your MySQL config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:Test123$67@touch.synology.me:3307/flaskdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 🔌 Initialize DB
    db.init_app(app)

    # 🔗 Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
