"""
Vercel entry point for ElectroStore Django app
"""
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electrostore.settings')

from electrostore.wsgi import application

# Vercel serverless handler
app = application
