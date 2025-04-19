from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # ✅ Import text

app = Flask(__name__)

# 🔧 Replace these with your actual values
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:Test123$67@touch.synology.me:3307/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def test_connection():
    try:
        db.session.execute(text('SELECT 1'))  # ✅ Use text()
        return '✅ Connected to MySQL successfully!'
    except Exception as e:
        return f'❌ Failed to connect to MySQL: {str(e)}'


if __name__ == '__main__':
    app.run(debug=True)
