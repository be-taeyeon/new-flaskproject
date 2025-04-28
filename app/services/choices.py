from app.models import db, Choice

# 선택지 생성 (특정 질문에 추가)
def create_choice(question_id, text):
    choice = Choice(question_id=question_id, text=text)
    db.session.add(choice)
    db.session.commit()
    return choice

# 선택지 전체 조회 (특정 질문 기준)
def get_choices_by_question_id(question_id):
    return Choice.query.filter_by(question_id=question_id).all()

# 선택지 하나 조회
def get_choice_by_id(choice_id):
    return Choice.query.get(choice_id)

# 선택지 수정
def update_choice(choice_id, new_text):
    choice = Choice.query.get(choice_id)
    if choice:
        choice.text = new_text
        db.session.commit()
        return choice
    return None

# 선택지 삭제
def delete_choice(choice_id):
    choice = Choice.query.get(choice_id)
    if choice:
        db.session.delete(choice)
        db.session.commit()
        return True
    return False
