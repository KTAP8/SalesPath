from flask import Blueprint, jsonify
from sqlalchemy import text
from . import db  # import from __init__.py
from .models import SalesMan

main = Blueprint("main", __name__)


@main.route('/')
def test_connection():
    try:
        db.session.execute(text('SELECT 1'))
        return '✅ Connected to MySQL successfully!'
    except Exception as e:
        return f'❌ Failed to connect to MySQL: {str(e)}'


@main.route('/api/salesmen', methods=['GET'])
def get_all_salesmen():
    try:
        salesmen = SalesMan.query.all()
        return jsonify([s.to_dict() for s in salesmen])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
