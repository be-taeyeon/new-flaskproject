from app import db
from app.models import User

# 1. 사용자 생성 (Create)
def create_user(username, email, password):
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

# 2. 사용자 조회 (Read)
def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_all_users():
    return User.query.all()

# 3. 사용자 정보 수정 (Update)
def update_user(user_id, new_username=None, new_email=None, new_password=None):
    user = get_user_by_id(user_id)
    if not user:
        return None  # 유저가 없으면 None 반환

    if new_username:
        user.username = new_username
    if new_email:
        user.email = new_email
    if new_password:
        user.password = new_password

    db.session.commit()
    return user

# 4. 사용자 삭제 (Delete)
def delete_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return False  # 유저가 없으면 삭제할 수 없음
    
    db.session.delete(user)
    db.session.commit()
    return True
