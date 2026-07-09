#!/bin/bash

echo "🚀 Deploying FileFormatProBot..."

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

# Start the application
gunicorn app:app --bind 0.0.0.0:8080

echo "✅ Deployment complete!"
