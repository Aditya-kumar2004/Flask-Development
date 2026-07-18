# Thiss folder iss package andd andd in this file we write only  database and import model

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.employee import Employee