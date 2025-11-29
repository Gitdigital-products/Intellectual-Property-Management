#!/usr/bin/env python3
"""
Database setup script for IP Management System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from src.models.ip_assets import Base
from config.settings import Config

def setup_database():
    """Initialize the database with required tables"""
    
    # Create engine and tables
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    
    print("Creating database tables...")
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")
    
    # Add initial data if needed
    print("Database setup completed!")

if __name__ == "__main__":
    setup_database()
