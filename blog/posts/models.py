from django.db import models
from django.contrib.auth import settings # 장고 기본 설정을 통해서 유저 모델 가져오기

# 처리할 데이터를 models.py에 정의

class Post(models.Model):
    title = models.CharField(max_length=200)                # models.CharField() : 짧은 문자열(제목)
    body = models.TextField()                               # models.TextField() : 긴 문자열(내용)
    img = models.ImageField(upload_to = 'posts/image')
    created_at = models.DateTimeField(auto_now_add = True)  # models.DateTimeField() : 날짜와 시간을 나타내는 데이터
    updated_at = models.DateTimeField(auto_now = True)

# 작성한 model을 DataBase에 적용하는 명령어 : python manage.py makemigrations
# model을 DataBase에 migrate : python manage.py migrate
# admin 계정 생성 : python manage.py createsuperuser
    def __str__(self):
        return self.title

    def summary(self):      # 본문의 내용을 100글자로 제한
        return self.body[:220]

# 댓글 모델
class Comment(models.Model): # 외래키는 다른 2차원 테이블과 연결 시켜주는 역할
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="comments") # related_name은 상대방에서 해당 모델을 인식하는 필드 이름
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 유저와의 1:N 구조의 연결
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text