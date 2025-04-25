from models import User, AgeStatus, GenderStatus
from config import db
from flask import abort

def create_user(name, age, gender, email):
    if User.query.filter_by(email=email).first():
        abort(400, "이미 존재하는 계정입니다.")
    
    new_user = User(
        name=name,
        age=AgeStatus(age),
        gender=GenderStatus(gender),
        email=email
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user.to_dict()

def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, "해당 유저를 찾을 수 없습니다.")
    return user.to_dict()
