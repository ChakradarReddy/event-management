#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting build process..."

# Upgrade pip first
pip install --upgrade pip

echo "📦 Installing dependencies..."
pip install -r requirements.txt

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
