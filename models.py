from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Joke(db.Model):
    """
    Represents a joke in the database.
    Attributes:
        id (int): The primary key of the joke.
        text (str): The text content of the joke.
        created_at (datetime): The timestamp when the joke was created.
        labels (list): A list of labels associated with the joke.
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    labels = db.relationship('Label', backref='joke', lazy=True)

class Visitor(db.Model):
    """
    Represents a visitor in the joke labeler application.
    Attributes:
        id (str): The unique identifier for the visitor, stored as a UUID.
        created_at (datetime): The timestamp when the visitor was created, defaults to the current UTC time.
        labels (list): A list of labels associated with the visitor, establishing a one-to-many relationship with the Label model.
    """
    id = db.Column(db.String(36), primary_key=True)  # UUID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    labels = db.relationship('Label', backref='visitor', lazy=True)

class Label(db.Model):
    """
    Represents a label for a joke in the joke labeling application.
    Attributes:
        id (int): The primary key of the label.
        joke_id (int): The foreign key referencing the joke being labeled.
        visitor_id (str): The foreign key referencing the visitor who labeled the joke.
        no_punchline (bool): Indicates whether the joke has no punchline.
        created_at (datetime): The timestamp when the label was created.
        segments (list): A list of LabelSegment objects associated with this label.
    """
    id = db.Column(db.Integer, primary_key=True)
    joke_id = db.Column(db.Integer, db.ForeignKey('joke.id'), nullable=False)
    visitor_id = db.Column(db.String(36), db.ForeignKey('visitor.id'), nullable=False)
    no_punchline = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    segments = db.relationship('LabelSegment', backref='label', lazy=True)

class LabelSegment(db.Model):
    """
    Represents a segment of text that has been labeled.
    Attributes:
        id (int): The primary key for the label segment.
        label_id (int): The foreign key referencing the label.
        start_index (int): The starting index of the labeled segment.
        end_index (int): The ending index of the labeled segment.
    """
    id = db.Column(db.Integer, primary_key=True)
    label_id = db.Column(db.Integer, db.ForeignKey('label.id'), nullable=False)
    start_index = db.Column(db.Integer, nullable=False)
    end_index = db.Column(db.Integer, nullable=False)
