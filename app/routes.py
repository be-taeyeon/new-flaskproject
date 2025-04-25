from flask import Blueprint, jsonify, request, abort, render_template, redirect, url_for, session, current_app
from flasgger import Swagger, swag_from
from app.models import User, Image, Question, Choices, Answer, Survey, ScoreRange
from config import db
import redis
from datetime import datetime

routes = Blueprint("routes", __name__)
redis_client = redis.Redis.from_url('redis://localhost:6379/0')

def get_signup_attempts(ip):
    """IP 주소별 가입 시도 횟수를 반환"""
    return int(redis_client.get(f'signup_attempts:{ip}') or 0)

def increment_signup_attempts(ip):
    """IP 주소별 가입 시도 횟수를 증가"""
    key = f'signup_attempts:{ip}'
    redis_client.incr(key)
    redis_client.expire(key, current_app.config['SIGNUP_WINDOW'])

# Swagger 설정
swagger = Swagger()

@routes.route("/", methods=["GET"])
def index():
    return redirect(url_for("routes.user_surveys"))

@routes.route("/image/main", methods=["GET"])
@swag_from({
    "responses": {
        200: {
            "description": "메인 이미지 가져오기",
            "examples": {"application/json": {"image": "https://example.com/image.jpg"}}
        }
    }
})
def get_main_image():
    return jsonify({"image": "https://example.com/image.jpg"})

@routes.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")

@routes.route("/surveys/<int:survey_id>/signup", methods=["GET"])
def survey_signup(survey_id):
    # survey_id 유효성 검사
    survey = Survey.query.get_or_404(survey_id)
    return render_template("signup.html", survey_id=survey_id)

@routes.route("/signup", methods=["POST"])
@swag_from({
    "tags": ["사용자"],
    "description": "회원가입",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "gender": {"type": "string"},
                    "email": {"type": "string"}
                }
            }
        }
    ],
    "responses": {
        201: {
            "description": "회원가입 성공",
            "examples": {
                "application/json": {
                    "message": "회원가입이 완료되었습니다.",
                    "user": {
                        "id": 1,
                        "name": "홍길동",
                        "age": 24,
                        "gender": "male",
                        "email": "hong@example.com"
                    }
                }
            }
        }
    }
})
def signup():
    data = request.get_json()
    client_ip = request.remote_addr
    
    try:
        # 이메일 중복 체크
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            increment_signup_attempts(client_ip)  # 실패한 시도만 카운트
            return jsonify({"error": "이미 등록된 이메일입니다."}), 400

        # 이메일이 존재하지 않는 경우에는 시도 횟수 체크를 하지 않고 바로 가입 진행
        user = User(
            name=data["name"],
            age=data["age"],
            gender=data["gender"],
            email=data["email"],
            ip_address=client_ip
        )
        db.session.add(user)
        db.session.commit()
        
        # 세션에 사용자 정보 저장
        session['user_id'] = user.id
        session['user_email'] = user.email
        
        # 설문 ID 처리
        survey_id = data.get("survey_id")
        if survey_id and survey_id != "null":  # survey_id가 있고 "null"이 아닌 경우
            return jsonify({
                "message": "회원가입이 완료되었습니다.",
                "user": user.to_dict(),
                "survey_id": int(survey_id)  # 정수로 변환
            })
        else:
            return jsonify({
                "message": "회원가입이 완료되었습니다.",
                "user": user.to_dict()
            })
            
    except Exception as e:
        db.session.rollback()
        increment_signup_attempts(client_ip)  # 실패한 시도만 카운트
        return jsonify({"error": str(e)}), 400

@routes.route("/questions/<int:question_id>", methods=["GET"])
def get_question(question_id):
    question = Question.query.get_or_404(question_id)
    return jsonify(question.to_dict())

@routes.route("/questions/count", methods=["GET"])
def get_question_count():
    total = Question.query.count()
    return jsonify({"total": total})

@routes.route("/choice/<int:question_id>", methods=["GET"])
def get_choices(question_id):
    choices = Choices.query.filter_by(question_id=question_id).all()
    return jsonify({"choices": [choice.to_dict() for choice in choices]})

@routes.route("/submit", methods=["POST"])
def submit_answers():
    # 로그인 확인
    if 'user_id' not in session:
        return jsonify({"error": "로그인이 필요합니다."}), 401
        
    # 사용자 존재 여부 확인
    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        session.clear()  # 잘못된 세션 정보 삭제
        return jsonify({"error": "유효하지 않은 사용자입니다. 다시 로그인해주세요."}), 401
    
    try:
        data = request.get_json()
        
        # 첫 번째 질문에서 설문 ID 가져오기
        if not data:
            return jsonify({"error": "응답이 없습니다."}), 400
            
        first_question = Question.query.get(data[0]["question_id"])
        if not first_question:
            return jsonify({"error": "유효하지 않은 질문입니다."}), 400
            
        survey = Survey.query.get(first_question.survey_id)
        
        for answer_data in data:
            # 질문과 선택지 존재 여부 확인
            question = Question.query.get(answer_data["question_id"])
            choice = Choices.query.get(answer_data["choice_id"])
            
            if not question or not choice or choice.question_id != question.id:
                return jsonify({"error": "유효하지 않은 질문 또는 선택지입니다."}), 400
            
            answer = Answer(
                user_id=user_id,
                question_id=answer_data["question_id"],
                choice_id=answer_data["choice_id"]
            )
            db.session.add(answer)
        
        db.session.commit()
        
        # 점수 계산 및 결과 페이지로 리다이렉트
        if survey.is_scored:
            return jsonify({
                "redirect": f"/surveys/{survey.id}/result"
            })
        else:
            return jsonify({
                "message": "설문이 제출되었습니다.",
                "redirect": "/surveys"
            })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "설문 제출 중 오류가 발생했습니다."}), 500

@routes.route("/surveys/<int:survey_id>/result")
def survey_result(survey_id):
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
        
    survey = Survey.query.get_or_404(survey_id)
    user_id = session['user_id']
    
    # 점수 계산
    score = survey.calculate_score(user_id)
    result_message = survey.get_result_message(score)
    
    # 사용자의 응답 내역 가져오기
    answers = []
    for question in survey.questions:
        answer = Answer.query.filter_by(
            user_id=user_id,
            question_id=question.id
        ).first()
        
        if answer:
            choice = Choices.query.get(answer.choice_id)
            answers.append({
                'question': question.title,
                'choice': choice.content,
                'score': choice.score if survey.is_scored else None
            })
    
    return render_template(
        'survey_result.html',
        survey=survey,
        score=score,
        result_message=result_message,
        answers=answers
    )

@routes.route("/image", methods=["POST"])
def create_image():
    data = request.get_json()
    image = Image(**data)
    db.session.add(image)
    db.session.commit()
    return jsonify({"message": f"ID: {image.id} Image Success Create"})

@routes.route("/question", methods=["POST"])
def create_question():
    data = request.get_json()
    question = Question(**data)
    db.session.add(question)
    db.session.commit()
    return jsonify({"message": f"Title: {question.title} question Success Create"})

@routes.route("/choice", methods=["POST"])
def create_choice():
    data = request.get_json()
    choice = Choices(**data)
    db.session.add(choice)
    db.session.commit()
    return jsonify({"message": f"Content: {choice.content} choice Success Create"})

@routes.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return render_template("users.html", users=users)

@routes.route("/surveys/new", methods=["GET"])
def new_survey():
    return render_template("create_survey.html")

@routes.route("/surveys", methods=["POST"])
def create_survey():
    try:
        data = request.get_json()
        print("Received data:", data)  # 디버깅을 위한 로그
        
        # Create new survey
        survey = Survey(
            title=data["title"],
            is_scored=data.get("is_scored", False)
        )
        db.session.add(survey)
        db.session.flush()  # Get survey.id before committing
        
        # Create score ranges if it's a scored survey
        if survey.is_scored and "score_ranges" in data:
            print("Creating score ranges:", data["score_ranges"])  # 디버깅을 위한 로그
            for range_data in data["score_ranges"]:
                score_range = ScoreRange(
                    survey_id=survey.id,
                    max_score=range_data["max_score"],
                    message=range_data["message"]
                )
                db.session.add(score_range)
                print(f"Added score range: max_score={range_data['max_score']}, message={range_data['message']}")
        
        # Create questions and choices
        for q_data in data["questions"]:
            question = Question(title=q_data["title"], survey_id=survey.id)
            db.session.add(question)
            db.session.flush()  # Get question.id before committing
            
            for c_data in q_data["choices"]:
                choice = Choices(
                    content=c_data["content"],
                    question_id=question.id,
                    score=c_data.get("score", 0)  # 점수가 없으면 0으로 설정
                )
                db.session.add(choice)
        
        db.session.commit()
        return jsonify({"id": survey.id})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating survey: {str(e)}")  # 서버 로그에 에러 출력
        return jsonify({"error": "설문조사 생성 중 오류가 발생했습니다."}), 500

@routes.route("/surveys", methods=["GET"])
def user_surveys():
    surveys = Survey.query.all()
    return render_template("user_surveys.html", surveys=surveys)

@routes.route("/admin", methods=["GET"])
def admin_index():
    # 통계 데이터 가져오기
    total_users = User.query.count()
    total_surveys = Survey.query.count()
    total_answers = Answer.query.count()
    
    # 최근 활동 가져오기
    recent_activities = [
        {
            "description": "새로운 사용자가 가입했습니다",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        },
        {
            "description": "새로운 설문조사가 생성되었습니다",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    ]
    
    return render_template("index.html",
                         total_users=total_users,
                         total_surveys=total_surveys,
                         total_answers=total_answers,
                         recent_activities=recent_activities)

@routes.route("/surveys/<int:survey_id>", methods=["GET"])
def get_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    if request.path.startswith('/admin'):
        return render_template("admin/survey_detail.html", survey=survey)
    return render_template("user/survey_detail.html", survey=survey)

@routes.route("/surveys/<int:survey_id>", methods=["DELETE"])
def delete_survey(survey_id):
    try:
        survey = Survey.query.get_or_404(survey_id)
        
        # 설문과 관련된 답변들 삭제
        for question in survey.questions:
            Answer.query.filter_by(question_id=question.id).delete()
            
        # 설문 삭제 (questions와 choices는 cascade 설정으로 자동 삭제됨)
        db.session.delete(survey)
        db.session.commit()
        
        return jsonify({"message": "설문조사가 삭제되었습니다."})
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting survey: {str(e)}")
        return jsonify({"error": "설문조사 삭제 중 오류가 발생했습니다."}), 500

@routes.route("/surveys/<int:survey_id>/edit", methods=["GET"])
def edit_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    return render_template("edit_survey.html", survey=survey)

@routes.route("/surveys/<int:survey_id>", methods=["PUT"])
def update_survey(survey_id):
    try:
        survey = Survey.query.get_or_404(survey_id)
        data = request.get_json()
        
        # Update survey title and scoring option
        survey.title = data["title"]
        survey.is_scored = data.get("is_scored", False)
        
        # Delete existing score ranges
        for range in survey.score_ranges:
            db.session.delete(range)
            
        # Create new score ranges if it's a scored survey
        if survey.is_scored and "score_ranges" in data:
            for range_data in data["score_ranges"]:
                score_range = ScoreRange(
                    survey_id=survey.id,
                    max_score=range_data["max_score"],
                    message=range_data["message"]
                )
                db.session.add(score_range)
        
        # Delete existing questions and choices
        for question in survey.questions:
            for choice in question.choices:
                db.session.delete(choice)
            db.session.delete(question)
        
        # Create new questions and choices
        for q_data in data["questions"]:
            question = Question(title=q_data["title"], survey_id=survey.id)
            db.session.add(question)
            db.session.flush()
            
            for c_data in q_data["choices"]:
                choice = Choices(
                    content=c_data["content"],
                    question_id=question.id,
                    score=c_data.get("score", 0) if survey.is_scored else 0
                )
                db.session.add(choice)
        
        db.session.commit()
        return jsonify({"id": survey.id})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating survey: {str(e)}")
        return jsonify({"error": "설문조사 수정 중 오류가 발생했습니다."}), 500

@routes.route("/surveys/<int:survey_id>/take", methods=["GET"])
def take_survey(survey_id):
    # 로그인 상태 확인
    if 'user_id' not in session:
        # 비로그인 상태면 회원가입 페이지로 리다이렉트
        return redirect(url_for('routes.survey_signup', survey_id=survey_id))
    
    survey = Survey.query.get_or_404(survey_id)
    return render_template("take_survey.html", survey=survey)

@routes.route("/admin/surveys", methods=["GET"])
def admin_surveys():
    surveys = Survey.query.all()
    return render_template("surveys.html", surveys=surveys)

@routes.route("/admin/surveys/<int:survey_id>", methods=["GET"])
def admin_survey_detail(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    return render_template("admin/survey_detail.html", survey=survey)

@routes.route("/admin/surveys/new", methods=["GET"])
def admin_new_survey():
    return render_template("create_survey.html")

@routes.route("/admin/surveys/<int:survey_id>/edit", methods=["GET"])
def admin_edit_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    return render_template("edit_survey.html", survey=survey)

@routes.route("/admin/users", methods=["GET"])
def admin_users():
    users = User.query.all()
    return render_template("users.html", users=users)

@routes.route("/admin/users/<int:user_id>/details", methods=["GET"])
def admin_user_details(user_id):
    user = User.query.get_or_404(user_id)
    
    # 사용자가 참여한 설문조사 조회
    completed_surveys = []
    answers = Answer.query.filter_by(user_id=user_id).all()
    survey_ids = set()
    
    for answer in answers:
        question = Question.query.get(answer.question_id)
        if question and question.survey_id not in survey_ids:
            survey = Survey.query.get(question.survey_id)
            if survey:
                survey_ids.add(question.survey_id)
                completed_surveys.append({
                    "id": survey.id,
                    "title": survey.title,
                    "completed_at": answer.created_at.strftime("%Y-%m-%d %H:%M")
                })
    
    return jsonify({
        "user": user.to_dict(),
        "surveys": completed_surveys
    })

@routes.route("/admin/users/<int:user_id>", methods=["DELETE"])
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # 사용자의 답변 삭제
    Answer.query.filter_by(user_id=user_id).delete()
    
    # 사용자 삭제
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "사용자가 성공적으로 삭제되었습니다."})

@routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    
    if user:
        session['user_id'] = user.id
        session['user_email'] = user.email
        return jsonify({"message": "로그인 성공", "user": user.to_dict()})
    else:
        return jsonify({"error": "사용자를 찾을 수 없습니다."}), 404

@routes.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('routes.index'))

@routes.route("/admin/surveys/<int:survey_id>/responses", methods=["GET"])
def admin_survey_responses(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    
    # 설문 응답 데이터 수집
    responses = []
    users_answered = set()
    
    # 각 질문에 대한 응답 수집
    for question in survey.questions:
        answers = Answer.query.filter_by(question_id=question.id).all()
        for answer in answers:
            users_answered.add(answer.user_id)
    
    # 사용자별 응답 데이터 수집
    for user_id in users_answered:
        user = User.query.get(user_id)
        if user:
            user_responses = []
            for question in survey.questions:
                answer = Answer.query.filter_by(
                    user_id=user_id,
                    question_id=question.id
                ).first()
                
                if answer:
                    choice = Choices.query.get(answer.choice_id)
                    user_responses.append({
                        'question': question.title,
                        'answer': choice.content if choice else '답변 없음'
                    })
            
            responses.append({
                'user': user,
                'responses': user_responses,
                'submitted_at': Answer.query.filter_by(user_id=user_id).first().created_at
            })
    
    return render_template(
        "survey_responses.html",
        survey=survey,
        responses=responses
    )