from app.models import db, Question, Choice

# 질문 생성
def create_question(test_type, text, choices):
    question = Question(test_type=test_type, text=text)
    db.session.add(question)
    db.session.commit()

    for choice_text in choices:
        choice = Choice(question_id=question.id, text=choice_text)
        db.session.add(choice)
    db.session.commit()

    return question

# 질문 전체 조회
def get_all_questions(test_type=None):
    query = Question.query
    if test_type:
        query = query.filter_by(test_type=test_type)
    return query.all()

# 특정 질문 조회
def get_question_by_id(question_id):
    return Question.query.get(question_id)

# 질문 수정
def update_question(question_id, new_text):
    question = Question.query.get(question_id)
    if question:
        question.text = new_text
        db.session.commit()
        return question
    return None

# 질문 삭제
def delete_question(question_id):
    question = Question.query.get(question_id)
    if question:
        # 먼저 선택지 삭제
        Choice.query.filter_by(question_id=question_id).delete()
        db.session.delete(question)
        db.session.commit()
        return True
    return False

# 선택지 조회 (질문 id 기준)
def get_choices_by_question_id(question_id):
    return Choice.query.filter_by(question_id=question_id).all()
