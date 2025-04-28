from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User

auth = Blueprint('auth', __name__)

# 로그인 페이지
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('로그인 실패: 사용자명 또는 비밀번호가 올바르지 않습니다.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

# 로그아웃 처리
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

