#!/bin/bash

# EventHub Deployment Script for Heroku
# This script automates the deployment process

echo "🚀 EventHub - College Event Management System"
echo "Deployment Script"
echo "=================="

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed!"
    echo "Please install it first:"
    echo "  macOS: brew install heroku/brew/heroku"
    echo "  Windows: Download from https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if git repository is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit - EventHub College Event Management System"
fi

# Check if Heroku app exists
if [ -z "$1" ]; then
    echo "❌ Please provide a Heroku app name!"
    echo "Usage: ./deploy.sh your-app-name"
    echo "Example: ./deploy.sh eventhub-college"
    exit 1
fi

APP_NAME=$1

echo "🎯 Deploying to Heroku app: $APP_NAME"

# Check if app exists, create if not
if ! heroku apps:info --app $APP_NAME &> /dev/null; then
    echo "📱 Creating new Heroku app: $APP_NAME"
    heroku create $APP_NAME
else
    echo "✅ Heroku app $APP_NAME already exists"
fi

# Set environment variables
echo "🔧 Setting environment variables..."
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))") --app $APP_NAME
heroku config:set FLASK_ENV=production --app $APP_NAME

# Add Heroku remote if not exists
if ! git remote | grep -q "heroku"; then
    echo "🔗 Adding Heroku remote..."
    heroku git:remote -a $APP_NAME
fi

# Deploy to Heroku
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy EventHub to production - $(date)"

echo "📤 Pushing to Heroku..."
git push heroku main

# Check deployment status
echo "🔍 Checking deployment status..."
if heroku ps --app $APP_NAME | grep -q "web.1.*up"; then
    echo "✅ Deployment successful!"
    echo "🌐 Your app is available at: https://$APP_NAME.herokuapp.com"
    
    # Open the app
    echo "🔗 Opening the app in your browser..."
    heroku open --app $APP_NAME
    
else
    echo "❌ Deployment failed!"
    echo "📋 Checking logs..."
    heroku logs --tail --app $APP_NAME
    exit 1
fi

echo ""
echo "🎉 EventHub has been successfully deployed to Heroku!"
echo ""
echo "📋 Next steps:"
echo "   1. Test all functionality on the live site"
echo "   2. Set up custom domain if needed"
echo "   3. Configure monitoring and alerts"
echo "   4. Set up database backups"
echo ""
echo "🔗 App URL: https://$APP_NAME.herokuapp.com"
echo "📊 Heroku Dashboard: https://dashboard.heroku.com/apps/$APP_NAME"
echo ""
echo "Good luck with your competition! 🏆"
