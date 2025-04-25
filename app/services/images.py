from app.models import Image
from config import db

# 이미지 생성 함수
def create_image(url, description=None):
    new_image = Image(url=url, description=description)
    db.session.add(new_image)
    db.session.commit()
    return new_image

# 이미지 조회 함수
def get_images():
    return Image.query.all()