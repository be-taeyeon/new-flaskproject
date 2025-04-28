from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# 앱 초기화
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hack@localhost.practice'

# 데이터베이스 객체
db = SQLAlchemy(app)

# Flask-Login 초기화
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'  # 로그인 페이지 URL 지정

# 로그인 사용자 로드 함수
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # User 모델에서 사용자를 불러옵니다

# 블루프린트 등록
from app.routes.auth_routes import auth
from app.routes.main_routes import main

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)