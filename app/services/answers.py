from app.models import db, Answer

# 답변 저장 (사용자가 질문에 대해 선택지 고름)
def create_answer(user_id, question_id, choice_id):
    answer = Answer(user_id=user_id, question_id=question_id, choice_id=choice_id)
    db.session.add(answer)
    db.session.commit()
    return answer

# 특정 사용자 답변 전체 조회
def get_answers_by_user_id(user_id):
    return Answer.query.filter_by(user_id=user_id).all()

# 특정 질문에 대한 사용자의 답변 조회
def get_answer_by_user_and_question(user_id, question_id):
    return Answer.query.filter_by(user_id=user_id, question_id=question_id).first()

# 답변 수정 (만약 선택지를 바꿔야 할 때)
def update_answer(answer_id, new_choice_id):
    answer = Answer.query.get(answer_id)
    if answer:
        answer.choice_id = new_choice_id
        db.session.commit()
        return answer
    return None

# 답변 삭제
def delete_answer(answer_id):
    answer = Answer.query.get(answer_id)
    if answer:
        db.session.delete(answer)
        db.session.commit()
        return True
    return False
