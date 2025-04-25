from flask import Blueprint, request, jsonify
from app.models import User, AgeStatus, GenderStatus
from config import db

user_bp = Blueprint("user", __name__)

# 회원가입 (POST /signup)
@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    age = data.get("age")
    gender = data.get("gender")

    # 이메일 중복 체크
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "이미 존재하는 계정 입니다."}), 400

    try:
        new_user = User(
            name=name,
            email=email,
            age=AgeStatus(age),
            gender=GenderStatus(gender)
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": f"{new_user.name}님 회원가입을 축하합니다",
            "user_id": new_user.id
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"회원가입 실패: {str(e)}"}), 500
