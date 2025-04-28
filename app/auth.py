from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        age = request.form.get('age')
        gender = request.form.get('gender')

        # 비밀번호 암호화
        hashed_password = generate_password_hash(password, method='sha256')

        # 사용자 객체 생성
        new_user = User(name=name, email=email, password=hashed_password, age=age, gender=gender)
        db.session.add(new_user)
        db.session.commit()

        # 회원가입 후 로그인 페이지로 리다이렉트
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.index'))  # 로그인 후 홈으로 이동

        return "로그인 실패! 이메일 또는 비밀번호가 잘못되었습니다.", 401
    
    return render_template('login.html')
