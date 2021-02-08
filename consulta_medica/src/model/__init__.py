
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create sql tables for our data models

class Consulta(db.Model):
    __tablename__ = 'consulta_medica_consulta'
    id = db.Column(
        db.String(64),
        primary_key=True
    )
    start_date = db.Column(
        db.DateTime(), 
        nullable=False
    )
    end_date = db.Column(
        db.DateTime()
    )
    physician_id = db.Column(
        db.String(64), 
        nullable=False
    )
    patient_id = db.Column(
        db.String(64), 
        nullable=False
    )
    price = db.Column(
        db.Numeric(17, 4), 
        nullable=False
    )