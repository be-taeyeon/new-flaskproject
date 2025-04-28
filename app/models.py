from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(50), nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    age      = db.Column(db.Date, nullable=False)
    gender   = db.Column(db.Enum('male','female', name='gender'), nullable=False)
    answers  = db.relationship('Answer', backref='user', lazy=True)

class Question(db.Model):
    __tablename__ = 'questions'
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    survey_type = db.Column(db.Enum('male','female', name='survey_type'), nullable=False)
    choices     = db.relationship('Choice', backref='question', lazy=True)

class Choice(db.Model):
    __tablename__ = 'choices'
    id          = db.Column(db.Integer, primary_key=True)
    choice_text = db.Column(db.String(200), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)

class Answer(db.Model):
    __tablename__ = 'answers'
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'),    nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'),nullable=False)
    choice_id   = db.Column(db.Integer, db.ForeignKey('choices.id'),  nullable=False)
