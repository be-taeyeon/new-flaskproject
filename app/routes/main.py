from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)

# 남자 질문 목록
questions_male = [
    {
        "id": 1,
        "text": "친구를 만났다는 여자의 말에 , 나 신경쓰지말고 재밌게 놀아! 의 뜻은? (남자어)",
        "choices": ["연락 꼬박꼬박 잘해라", "진짜 나 신경쓰지 말고 놀아", "적당히 놀다가 나랑 놀자", "답장 빨링 안하기만 해봐 죽었어 아주"]
    },
    {
        "id": 2,
        "text": "게임 한 판 더 하고 자려고~ 라고 말한 남자의 결과는? (남자어)",
        "choices": ["진짜 한 판만 하고 잠", "최소 두 세판 더 할 예정", "이기면 찐막, 지면 이길 때까지", "하고 싶을 떄까지 함"]
    },
    {
        "id": 3,
        "text": "와 오늘 너무 피곤하다, 일찍 자야겠다. 라고 말한 후 이어지는 행동은? (남자어)",
        "choices": ["카톡 답장을 기다린다.", "진짜 바로 잔다.", "게임하러 간다.", "자기전 최후의 유튜브를 킨다."]
    }
]

# 여자 질문 목록
questions_female = [
    {
        "id": 1,
        "text": "친구를 만났다는 남자의 말에 , 나 신경쓰지말고 재밌게 놀아! 의 뜻은?  (여자어)",
        "choices": ["연락 꼬박꼬박 잘해라", "진짜 나 신경쓰지 말고 놀아", "적당히 놀다가 나랑 놀자", "답장 빨링 안하기만 해봐 죽었어 아주"]
    },
    {
        "id": 2,
        "text": "연인끼리 데이트 중 여자가 그 옷 또 입었네 ? 되게 좋아하나 봐의 숨은 뜻은? (여자어)",
        "choices": ["진짜로 되게 좋아하는 지 궁금함", "제발 갖다 버리고 그만 좀 입어", "옷 진짜 잘 어울린다", "옷이 그거 밖에 없어?"]
    },
    {
        "id": 3,
        "text": "이별 후의 여자가 그동안 고마웠어, 좋은사람 만나고 행복해 의 숨은 뜻은? (여자어)",
        "choices": ["정말 고마웠어, 행복하길바래", "나 같은 사람 못 만나니 평생 후회하길 바람", "형식적으로 걍 말한거니 신경쓰지마삼"]
    }
]

# 성별에 따라 질문 세트 선택
@main.route('/survey/<int:question_id>/<gender>', methods=['GET', 'POST'])
def survey(question_id, gender):
    if gender not in ['male', 'female']:
        return redirect(url_for('main.result'))  # 잘못된 성별 값 처리

    # 성별에 맞는 질문 세트 선택
    if gender == 'male':
        questions = questions_male
    else:
        questions = questions_female

    if request.method == 'POST':
        selected = request.form.get("answer")
        print(f"Q{question_id} ({gender}): {selected}")

        next_question_id = question_id + 1
        if next_question_id > len(questions):
            return redirect(url_for('main.result'))
        return redirect(url_for('main.survey', question_id=next_question_id, gender=gender))

    question = questions[question_id - 1]
    return render_template('survey.html', question=question, gender=gender)