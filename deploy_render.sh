#!/bin/bash

# EventHub Deployment Script for Render
# This script prepares your app for Render deployment

echo "🚀 EventHub - College Event Management System"
echo "Render Deployment Script"
echo "========================"

# Check if git repository is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found!"
    echo "Please initialize git first:"
    echo "  git init"
    echo "  git add ."
    echo "  git commit -m 'Initial commit'"
    exit 1
fi

# Check if remote origin exists
if ! git remote | grep -q "origin"; then
    echo "❌ No GitHub remote found!"
    echo "Please add your GitHub repository as origin:"
    echo "  git remote add origin https://github.com/yourusername/yourrepo.git"
    exit 1
fi

echo "✅ Git repository ready"
echo "📤 Pushing to GitHub..."

# Push to GitHub
git push origin main

echo ""
echo "🎉 Code pushed to GitHub successfully!"
echo ""
echo "📋 Next steps to deploy on Render:"
echo "   1. Go to https://dashboard.render.com/"
echo "   2. Sign up/Login with GitHub"
echo "   3. Click 'New +' → 'Web Service'"
echo "   4. Connect your GitHub repository"
echo "   5. Select 'college_event_system'"
echo "   6. Use these settings:"
echo "      - Name: college-event-system"
echo "      - Environment: Python"
echo "      - Build Command: ./build.sh"
echo "      - Start Command: gunicorn app:app"
echo "      - Plan: Free"
echo "   7. Click 'Create Web Service'"
echo ""
echo "🔗 Your app will be available at: https://college-event-system.onrender.com"
echo "⏱️  First deployment may take 5-10 minutes"
echo ""
echo "Good luck with your competition! 🏆"
