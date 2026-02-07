from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from . import routes  # Import routes at the bottom to avoid circular imports
from .models_extended import Agent, Career, Consultation, Contact, Property, Valuation  # Import new models

# Create database tables if they don't exist
def create_database():
    with app.app_context():
        db.create_all()

create_database()
