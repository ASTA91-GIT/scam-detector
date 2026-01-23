"""
Database Configuration and Models
"""
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
client = None
db = None

def init_db():
    """Initialize MongoDB connection"""
    global client, db
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    database_name = os.getenv('DATABASE_NAME', 'job_scam_detector')
    
    try:
        client = MongoClient(mongodb_uri)
        db = client[database_name]
        # Test connection
        client.admin.command('ping')
        print(f"✓ Connected to MongoDB: {database_name}")
        
        # Create indexes for better performance
        db.users.create_index('email', unique=True)
        db.analyses.create_index('user_id')
        db.analyses.create_index('created_at')
        
    except Exception as e:
        print(f"✗ MongoDB connection error: {e}")
        raise

def get_db():
    """Get database instance"""
    return db

def get_users_collection():
    """Get users collection"""
    return db.users

def get_analyses_collection():
    """Get analyses collection"""
    return db.analyses

def get_files_collection():
    """Get uploaded_files collection"""
    return db.uploaded_files
