from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    survey_type = db.Column(db.String(50))  # '남자어' 또는 '여자어'
    choices = db.relationship('Choice', backref='question')

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice_text = db.Column(db.String(200))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    choice_id = db.Column(db.Integer, db.ForeignKey('choice.id'))