from flask import Flask, Blueprint, session, render_template, request, redirect, url_for
import os
from werkzeug.security import generate_password_hash, check_password_hash
from config import db
from app.models import User
from flask import flash
# Flask 애플리케이션 생성
main = Blueprint('main', __name__)

# 애플리케이션 초기화 후 바로 secret_key 설정
main.secret_key = os.urandom(24)  # 또는 app.config['SECRET_KEY'] = os.urandom(24)

@main.route('/')
def index():
    return render_template('index.html')


# 회원가입 페이지
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # 회원가입 처리 로직
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # 비밀번호 해싱
        hashed_password = generate_password_hash(password)
        
        # DB에 사용자 정보 저장
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('main.index'))  # 회원가입 후 메인 페이지로 이동
    
    return render_template('signup.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # 로그인된 사용자 ID 세션에 저장
            return redirect(url_for('main.index'))  # 로그인 후 메인 페이지로 이동
        else:
            flash('로그인 실패: 이메일 또는 비밀번호를 확인해주세요.', 'danger')
    
    return render_template('login.html')



@main.route('/quiz/<gender>', methods=['GET', 'POST'])
def quiz(gender):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))  # 로그인되지 않은 사용자에게 로그인 페이지로 리다이렉트
    
    question = "질문 예시입니다. 어떤 답변을 고르시겠어요?"
    
    if request.method == 'POST':
        # 답변 처리 로직
        return redirect(url_for('main.index'))  # 퀴즈 종료 후 메인 페이지로 이동
    
    return render_template('quiz.html', gender=gender, question=question)


# 로그아웃 페이지
@main.route('/logout')
def logout():
    session.pop('user_id', None)  # 세션에서 user_id 삭제
    return redirect(url_for('main.index'))

if __name__ == '__main__':
    main.run(debug=True)
