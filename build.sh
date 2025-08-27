#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Create uploads directory if it doesn't exist
mkdir -p uploads

# Initialize database if it doesn't exist
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database initialized successfully!')
"
