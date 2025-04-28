from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User, Question, Choice, Answer
from flask_login import login_required, current_user
from sqlalchemy import func

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('index.html', name=current_user.name)

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

@main.route('/survey_complete')
@login_required
def survey_complete():
    return render_template('survey_complete.html')

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