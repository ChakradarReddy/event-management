#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting build process..."

# Upgrade pip first
pip install --upgrade pip

echo "📦 Installing dependencies..."
# Install packages one by one to identify any issues
pip install Flask==2.3.3
pip install Flask-SQLAlchemy==3.0.5
pip install Flask-Login==0.6.3
pip install Flask-WTF==1.1.1
pip install WTForms==3.0.1
pip install Werkzeug==2.3.7
pip install Pillow==9.5.0
pip install python-dotenv==1.0.0
pip install gunicorn==21.2.0
pip install email-validator==2.0.0
pip install bcrypt==4.0.1
pip install reportlab==3.6.12

# Create uploads directory if it doesn't exist
mkdir -p uploads

echo "🗄️ Initializing database..."
# Initialize database if it doesn't exist
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Database initialized successfully!')
"

echo "✅ Build completed successfully!"
