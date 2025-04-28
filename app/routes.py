from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from app.models import User, Question, Choice, Answer
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

main = Blueprint('main', __name__)

# 홈 페이지
@main.route('/')
@login_required
def index():
    return render_template('index.html', name=current_user.name)

# 회원가입 페이지
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['password']
        age = request.form['age']
        gender = request.form['gender']
        hashed = generate_password_hash(pwd, method='pbkdf2:sha256')
        user = User(name=name, email=email, password=hashed, age=age, gender=gender)
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('main.index'))
        except:
            db.session.rollback()
            flash('이미 등록된 이메일입니다.', 'danger')
    return render_template('signup.html')

# 로그인 페이지
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, pwd):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('로그인 실패: 이메일 또는 비밀번호 확인', 'danger')
    return render_template('login.html')

# 로그아웃
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# 설문 시작 페이지 (남자어/여자어 선택)
@main.route('/survey/<survey_type>', methods=['GET', 'POST'])
@login_required
def survey(survey_type):
    questions = Question.query.filter_by(survey_type=survey_type).all()
    if request.method == 'POST':
        for q in questions:
            cid = request.form.get(f'question_{q.id}')
            if cid:
                db.session.add(Answer(user_id=current_user.id, question_id=q.id, choice_id=int(cid)))
        db.session.commit()
        return redirect(url_for('main.survey_complete'))
    return render_template('survey.html', questions=questions, survey_type=survey_type)

# 설문 완료 페이지
@main.route('/survey_complete')
@login_required
def survey_complete():
    return render_template('survey_complete.html')

# 설문 결과 페이지
@main.route('/survey_results/<survey_type>')
@login_required
def survey_results(survey_type):
    qs = Question.query.filter_by(survey_type=survey_type).all()
    results = {}
    for q in qs:
        avg = db.session.query(func.avg(Answer.choice_id)).filter(Answer.question_id == q.id).scalar()
        top = db.session.query(Choice.choice_text, func.count(Answer.id).label('cnt'))\
            .join(Answer, Answer.choice_id == Choice.id)\
            .filter(Choice.question_id == q.id)\
            .group_by(Choice.id)\
            .order_by(func.count(Answer.id).desc())\
            .first()
        results[q.title] = {'average': avg, 'top': top}
    return render_template('survey_results.html', results=results, survey_type=survey_type)

# 개별 질문 페이지 (다음 질문으로 이동)
@main.route('/next_question/<int:question_id>')
@login_required
def next_question(question_id):
    question = Question.query.get_or_404(question_id)
    questions = Question.query.filter_by(survey_type=question.survey_type).all()
    total = len(questions)
    current_idx = questions.index(question) + 1

    return render_template(
        'survey_question.html',
        question=question,
        survey_type=question.survey_type,
        current_question=current_idx,
        total_questions=total
    )