#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting fallback build process (without Pillow)..."

# Force Python version check
python --version

# Upgrade pip first
pip install --upgrade pip

echo "📦 Installing essential dependencies..."
# Install only essential packages without Pillow
pip install Flask==3.0.0
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-Login==0.6.3
pip install Flask-WTF==1.2.1
pip install WTForms==3.1.1
pip install Werkzeug==3.0.1
pip install python-dotenv==1.0.0
pip install gunicorn==21.2.0
pip install email-validator==2.1.0
pip install bcrypt==4.1.2
pip install reportlab==4.0.7

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

echo "⚠️ Build completed without Pillow - image upload functionality will be limited"
echo "✅ Essential functionality should work fine"
