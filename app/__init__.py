from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hack@localhost/practice'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 확장 초기화
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # 모델 임포트 (필수)
    from app import models

    # 테이블이 없으면 자동 생성 (개발 전용)
    with app.app_context():
        db.create_all()

    # 사용자 로드 함수
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 블루프린트 등록
    from app.routes import main
    app.register_blueprint(main)

    return app
