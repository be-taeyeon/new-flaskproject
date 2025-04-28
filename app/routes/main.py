from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)

# 남자 질문 목록
questions_male = [
    {
        "id": 1,
        "text": "1. 당신이 아침에 가장 먼저 하는 일은? (남자어)",
        "choices": ["눈물 닦기", "폰 보기", "다시 자기", "세상에 화내기", "아무 생각 안 하기"]
    },
    {
        "id": 2,
        "text": "2. 가장 좋아하는 라면 종류는? (남자어)",
        "choices": ["신라면", "진라면", "너구리", "안 먹음", "컵라면 물 버릴 때 속상함"]
    },
    {
        "id": 3,
        "text": "3. 외계인이 나타나면? (남자어)",
        "choices": ["친구하자고 한다", "도망간다", "같이 사진 찍는다", "기절한다", "배달 시킨다"]
    }
]

# 여자 질문 목록
questions_female = [
    {
        "id": 1,
        "text": "1. 당신이 아침에 가장 먼저 하는 일은? (여자어)",
        "choices": ["눈물 닦기", "폰 보기", "다시 자기", "세상에 화내기", "아무 생각 안 하기"]
    },
    {
        "id": 2,
        "text": "2. 가장 좋아하는 라면 종류는? (여자어)",
        "choices": ["신라면", "진라면", "너구리", "안 먹음", "컵라면 물 버릴 때 속상함"]
    },
    {
        "id": 3,
        "text": "3. 외계인이 나타나면? (여자어)",
        "choices": ["친구하자고 한다", "도망간다", "같이 사진 찍는다", "기절한다", "배달 시킨다"]
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