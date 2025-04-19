from flask import Blueprint
from sqlalchemy import text
from . import db  # import from __init__.py

main = Blueprint("main", __name__)


@main.route('/')
def test_connection():
    try:
        db.session.execute(text('SELECT 1'))
        return '✅ Connected to MySQL successfully!'
    except Exception as e:
        return f'❌ Failed to connect to MySQL: {str(e)}'
