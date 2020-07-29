from django import forms # 장고에서 forms 모듈 import
from .models import Post, Comment # 모델에서 Post, Comment를 임포트

class BlogPost(forms.ModelForm): # 모델 폼클래스를 이용해서 Post모델로 간단히 필드 작성
    class Meta:
        model = Post # 호환될 모델 클래스
        fields = ['title', 'body', 'img'] # 작성할 Post의 필드들

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']