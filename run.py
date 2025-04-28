from flask import Flask
from app.routes.auth_routes import auth  # auth_routes에서 auth 블루프린트 임포트
from app.routes.main_routes import main  # main_routes에서 main 블루프린트 임포트

app = Flask(__name__)

# 블루프린트 등록
app.register_blueprint(auth, url_prefix='/auth')  # /auth로 접속 시 auth 라우트로 접근
app.register_blueprint(main)  # 기본 URL로 main 라우트로 접근

if __name__ == '__main__':
    app.run(debug=True)