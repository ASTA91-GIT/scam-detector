"""
Database Configuration and Models
"""
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

client = None
db = None

def init_db():
    """Initialize MongoDB connection"""
    global client, db

    mongodb_uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("DATABASE_NAME", "job_scam_detector")

    try:
        client = MongoClient(mongodb_uri)
        db = client[database_name]

        # Test connection
        client.admin.command("ping")
        print(f"✓ Connected to MongoDB: {database_name}")

        # Indexes
        db.users.create_index("email", unique=True)
        db.analyses.create_index("created_at")
        db.offers.create_index("risk_level")

    except Exception as e:
        print(f"✗ MongoDB connection error: {e}")
        raise


def get_db():
    return db

def get_users_collection():
    return db.users

def get_analyses_collection():
    return db.analyses

def get_offers_collection():
    return db.offers

def get_files_collection():
    return db.uploaded_files
