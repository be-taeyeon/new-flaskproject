from datetime import datetime
from zoneinfo import ZoneInfo
from flask import abort
from config import db
from sqlalchemy.orm import relationship
from sqlalchemy.sql import and_

KST = ZoneInfo("Asia/Seoul")

class CommonModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class User(CommonModel):
    __tablename__ = "users"
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6도 저장 가능하도록 45자로 설정

    __table_args__ = (
        db.CheckConstraint("age >= 0 AND age <= 120", name="check_age"),
        db.CheckConstraint("gender IN ('male', 'female')", name="check_gender"),
    )

    def __init__(self, name, age, gender, email, ip_address=None):
        if User.query.filter_by(email=email).first():
            abort(400, "이미 존재하는 계정 입니다.")

        try:
            age = int(age)
            if not (0 <= age <= 120):
                abort(400, f"Invalid age: {age}. Age must be between 0 and 120")
        except ValueError:
            abort(400, f"Invalid age format: {age}. Age must be a number")

        allowed_genders = {"male", "female"}
        if gender not in allowed_genders:
            abort(400, f"Invalid gender: {gender}. Allowed values: {allowed_genders}")

        self.name = name
        self.age = age
        self.gender = gender
        self.email = email
        self.ip_address = ip_address

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "email": self.email,
            "ip_address": self.ip_address,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# 설문 테이블
class Survey(CommonModel):
    __tablename__ = "surveys"
    title = db.Column(db.String(200), nullable=False)
    is_scored = db.Column(db.Boolean, default=False)  # 점수 기반 설문 여부
    score_ranges = db.relationship('ScoreRange', backref='survey', lazy=True, cascade="all, delete-orphan")
    questions = db.relationship("Question", backref="survey", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "is_scored": self.is_scored,
            "score_ranges": [range.to_dict() for range in self.score_ranges],
            "questions": [question.to_dict() for question in self.questions],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def calculate_score(self, user_id):
        if not self.is_scored:
            return None
            
        total_score = 0
        for question in self.questions:
            answer = Answer.query.filter_by(
                user_id=user_id,
                question_id=question.id
            ).first()
            
            if answer:
                choice = Choices.query.get(answer.choice_id)
                if choice:
                    total_score += choice.score
                    
        return total_score
        
    def get_result_message(self, score):
        if not self.is_scored or score is None:
            return "설문에 참여해주셔서 감사합니다."
            
        # 점수 구간이 없는 경우
        if not self.score_ranges:
            return f"총점: {score}점"
            
        # 점수 구간에 따른 결과 메시지 반환
        ranges = sorted(self.score_ranges, key=lambda x: x.max_score)
        
        # 가장 낮은 구간보다 낮은 경우
        if score < ranges[0].max_score:
            return ranges[0].message
            
        # 중간 구간들 확인
        for i in range(1, len(ranges)):
            if score < ranges[i].max_score:
                return ranges[i].message
                
        # 모든 구간보다 높은 점수인 경우 마지막 구간의 메시지 반환
        return ranges[-1].message

class Question(CommonModel):
    __tablename__ = "questions"
    title = db.Column(db.String(200), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey("surveys.id"), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"))  # Image와의 관계를 위한 외래키 추가
    choices = db.relationship("Choices", backref="question", lazy=True, cascade="all, delete-orphan")

    # Image와의 관계 설정
    image = db.relationship("Image", back_populates="questions")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "choices": [choice.to_dict() for choice in self.choices],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

class Choices(CommonModel):
    __tablename__ = "choices"
    content = db.Column(db.String(200), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    score = db.Column(db.Integer, default=0)  # 선택지별 점수

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "score": self.score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

# 응답 테이블
class Response(db.Model):
    __tablename__ = "responses"
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey("surveys.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    choice_id = db.Column(db.Integer, db.ForeignKey("choices.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Image(CommonModel):
    __tablename__ = "images"
    url = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    questions = db.relationship("Question", back_populates="image")

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

class Answer(CommonModel):
    __tablename__ = "answers"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    choice_id = db.Column(db.Integer, db.ForeignKey("choices.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "question_id": self.question_id,
            "choice_id": self.choice_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

class ScoreRange(db.Model):
    __tablename__ = "score_ranges"
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    max_score = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(500), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "max_score": self.max_score,
            "message": self.message,
        }