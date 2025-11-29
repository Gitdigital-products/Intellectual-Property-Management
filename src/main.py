#!/usr/bin/env python3
"""
Main application entry point for IP Management System
"""

from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import config
from src.api.routes import register_routes
from src.models.ip_assets import Base

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Setup database
    engine = create_engine(app.con
