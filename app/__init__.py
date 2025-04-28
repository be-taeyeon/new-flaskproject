from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # config.py에서 설정을 불러옴
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # 라우트 등록
    from .routes import main  # 여기서 라우트를 가져옵니다
    app.register_blueprint(main)  # 라우트를 등록

    return app
