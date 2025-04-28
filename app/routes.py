from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from app.models import Question, Answer, Choices
from flask_login import current_user, login_required
from sqlalchemy import func

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template("index.html")  # index.html 파일을 작성하여 메인 페이지를 제공

@main.route('/survey/male', methods=['GET', 'POST'])
@login_required
def male_survey():
    # 'male'로 분류된 설문을 진행
    questions = Question.query.filter_by(survey_type="male", is_active=True).all()
    return render_template("survey_male.html", questions=questions)

@main.route('/survey/female', methods=['GET', 'POST'])
@login_required
def female_survey():
    # 'female'로 분류된 설문을 진행
    questions = Question.query.filter_by(survey_type="female", is_active=True).all()
    return render_template("survey_female.html", questions=questions)

@main.route('/submit_answer/<int:question_id>', methods=['POST'])
@login_required
def submit_answer(question_id):
    choice_id = request.form.get("choice_id")
    choice = Choices.query.get_or_404(choice_id)
    
    # 답변 저장
    answer = Answer(user_id=current_user.id, choice_id=choice.id, question_id=question_id, answer=choice.choice_text, survey_type=choice.question.survey_type)
    db.session.add(answer)
    db.session.commit()

    # 다음 질문으로 이동 (여기서는 질문이 1개씩 표시됨)
    return redirect(url_for('main.next_question', question_id=question_id + 1))

@main.route('/next_question/<int:question_id>', methods=['GET'])
@login_required
def next_question(question_id):
    question = Question.query.get(question_id)
    if not question:
        return redirect(url_for('main.survey_complete'))

    return render_template('survey_question.html', question=question)

@main.route('/survey_complete')
@login_required
def survey_complete():
    return render_template("survey_complete.html")

@main.route('/survey/results/<survey_type>', methods=['GET'])
@login_required
def survey_results(survey_type):
    # 설문 유형에 따른 평균 계산
    questions = Question.query.filter_by(survey_type=survey_type).all()
    result_data = {}
    
    for question in questions:
        avg_answer = db.session.query(func.avg(Answer.answer)).filter(Answer.question_id == question.id).scalar()
        most_selected_choice = db.session.query(
            Choices.choice_text, 
            func.count(Answer.choice_id).label('count')
        ).join(Answer, Answer.choice_id == Choices.id).filter(Choices.question_id == question.id).group_by(Choices.id).order_by(func.count(Answer.choice_id).desc()).first()

        result_data[question.title] = {
            'average': avg_answer,
            'most_selected': most_selected_choice
        }

    return render_template('survey_results.html', result_data=result_data)
