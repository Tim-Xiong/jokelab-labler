from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Joke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    labels = db.relationship('Label', backref='joke', lazy=True)

class Visitor(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # UUID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    labels = db.relationship('Label', backref='visitor', lazy=True)

class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    joke_id = db.Column(db.Integer, db.ForeignKey('joke.id'), nullable=False)
    visitor_id = db.Column(db.String(36), db.ForeignKey('visitor.id'), nullable=False)
    no_punchline = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    segments = db.relationship('LabelSegment', backref='label', lazy=True)

class LabelSegment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label_id = db.Column(db.Integer, db.ForeignKey('label.id'), nullable=False)
    start_index = db.Column(db.Integer, nullable=False)
    end_index = db.Column(db.Integer, nullable=False)
