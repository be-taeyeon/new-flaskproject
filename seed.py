# seed.py
from app import create_app, db
from app.models import Question, Choice

app = create_app()

with app.app_context():
    # 1) 기존 데이터 전부 삭제 (테스트용)
    db.session.query(Choice).delete()
    db.session.query(Question).delete()
    db.session.commit()

    # 2) 남자어 문항 추가
    q1 = Question(title="1. 친구를 만났다는 여자의 말에 , 나 신경쓰지말고 재밌게 놀아! 의 뜻은?", survey_type="male")
    q2 = Question(title="2. 게임 한 판 더 하고 자려고~ 라고 말한 남자의 결과는?", survey_type="male")
    q3 = Question(title="3. 와 오늘 너무 피곤하다, 일찍 자야겠다. 라고 말한 후 이어지는 행동은?", survey_type="male")
    db.session.add_all([q1, q2, q3])
    db.session.flush()  # q1.id, q2.id 얻기

    choices = [
        Choice(choice_text="연락 꼬박꼬박 잘해라",    question_id=q1.id),
        Choice(choice_text="진짜 나 신경쓰지 말고 놀아", question_id=q1.id),
        Choice(choice_text="적당히 놀다가 나랑 놀자",    question_id=q1.id),
        Choice(choice_text="답장 빨링 안하기만 해봐 죽었어 아주",    question_id=q1.id),

        Choice(choice_text="진짜 한 판만 하고 잠",          question_id=q2.id),
        Choice(choice_text="최소 두 세판 더 할 예정",   question_id=q2.id),
        Choice(choice_text="이기면 찐막, 지면 이길 때까지", question_id=q2.id),
        Choice(choice_text="하고 싶을 떄까지 함", question_id=q2.id),

        Choice(choice_text="카톡 답장을 기다린다",          question_id=q3.id),
        Choice(choice_text="진짜 바로 잔다",   question_id=q3.id),
        Choice(choice_text="게임하러 간다", question_id=q3.id),
        Choice(choice_text="자기전 최후의 유튜브를 킨다", question_id=q3.id),
    ]
    db.session.add_all(choices)

    # 3) 여자어 문항 추가
    q3 = Question(title="1. 친구를 만났다는 여자의 말에 , 나 신경쓰지말고 재밌게 놀아! 의 뜻은?", survey_type="female")
    q4 = Question(title="2. 연인끼리 데이트 중 여자가 그 옷 또 입었네 ? 되게 좋아하나 봐의 숨은 뜻은?", survey_type="female")
    q5 = Question(title="3. 이별 후의 여자가 그동안 고마웠어, 좋은사람 만나고 행복해 의 숨은 뜻은?", survey_type="female")
    db.session.add_all([q3, q4, q5])
    db.session.flush()

    choices = [
        Choice(choice_text="연락 꼬박꼬박 잘해라", question_id=q3.id),
        Choice(choice_text="진짜 나 신경쓰지 말고 놀아", question_id=q3.id),
        Choice(choice_text="적당히 놀다가 나랑 놀자", question_id=q3.id),
        Choice(choice_text="답장 빨링 안하기만 해봐 죽었어 아주", question_id=q3.id),

        Choice(choice_text="진짜로 되게 좋아하는 지 궁금함",        question_id=q4.id),
        Choice(choice_text="제발 갖다 버리고 그만 좀 입어", question_id=q4.id),
        Choice(choice_text="이 옷 진짜 잘 어울린다",    question_id=q4.id),
        Choice(choice_text="옷이 그거 밖에 없어?",    question_id=q4.id),

        Choice(choice_text="정말 고마웠어, 행복하길바래",        question_id=q5.id),
        Choice(choice_text="나 같은 사람 못 만나니 평생 후회하길 바람", question_id=q5.id),
        Choice(choice_text="형식적으로 걍 말한거니 신경쓰지마삼",    question_id=q5.id),

    ]
    db.session.add_all(choices)

    # 4) 커밋
    db.session.commit()
    print("✅ Seed data inserted.")
