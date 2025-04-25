from app.models import Question, Choice
from config import db

# 질문 생성 함수
def create_question(text, choices):
    new_question = Question(text=text)
    db.session.add(new_question)
    db.session.flush()  # ID를 얻기 위해 flush

    for choice_text in choices:
        new_choice = Choice(question_id=new_question.id, text=choice_text)
        db.session.add(new_choice)

    db.session.commit()
    return new_question

# 질문 조회 함수
def get_questions():
    return Question.query.all()