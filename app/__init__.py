# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from app.routes import main

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)  # Flask 애플리케이션 객체 생성
    app.config.from_object(Config)  # Config에서 설정 가져오기

    # 랜덤하게 secret_key를 설정
    app.secret_key = os.urandom(24)  # 24 바이트 랜덤 값

    db.init_app(app)  # SQLAlchemy 초기화
    migrate.init_app(app, db)  # Migrate 초기화

    app.register_blueprint(main)  # Blueprint 등록

    return app
