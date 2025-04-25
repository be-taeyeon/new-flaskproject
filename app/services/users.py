from app.models import User
from config import db

# 유저 생성 함수
def create_user(name, email):
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return new_user

# 유저 조회 함수
def get_users():
    return User.query.all()