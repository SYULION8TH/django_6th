# Django 6회차
- [x] Comment
- [x] Update
- [x] Delete

# 댓글 모델 추가
## models.py
import 할 것
```python
from django.contrib.auth import settings # 장고 기본 설정을 통해서 유저 모델 가져오기
```
댓글 모델 추가
```python
# 댓글 모델
class Comment(models.Model): # 외래키는 다른 2차원 테이블과 연결 시켜주는 역할
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="comments") # related_name은 상대방에서 해당 모델을 인식하는 필드 이름
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 유저와의 1:N 구조의 연결
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
```

# 댓글 읽기(Read)
## detail.html
```html
    <!-- 댓글 목록 -->
    <div class="card mb-2">
        <h5 class="mt-0" style="padding-left: 20px; padding-top: 20px">댓글</h5>
        <div class="card-body">
            {% for comment in post.comments.all %} <!-- post에 comments필드가 생기고 그 comments의 모든 것을 가져온다. -->
            <div class="card mb-2">
                <div class="card-body">
                    <div class="media">
                        <div class="media-body">
                            <small class="text-muted">작성일 | {{comment.created_at}}</small>
                            <p>{{ comment.author }}: {{ comment.text }}</p>
                            <!-- 댓글 수정, 삭제 버튼 -->
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    <!-- 댓글 목록 -->
</div>
<!-- //글목록 card -->
<!-- 댓글 작성 링크 -->
<div class='container'>
    <a href="{% url 'comment_new' post.id %}" class="btn btn-primary">댓글 작성</a>
</div>
```
읽을 준비는 끝났습니다.
# 댓글 생성(Create)
## comment_new.html 생성
```html
{% extends 'base.html' %}
{% block contents %}
<!--content -->
<div class='container' style="padding-top: 4rem;">
    <form method = 'post' enctype="multipart/form-data">
        {% csrf_token %}
        <table>
            {{form.as_table}}
        </table>
        <br>
        <input class="btn btn-dart" type = "submit" value = "제출하기">
    </form>
</div>
<!-- //content -->
{% endblock %}
```
## forms.py에서 댓글 폼 상자를 위한 class 생성
바꿔야할 코드
```python
from .models import Post, Comment # 모델에서 Post, Comment를 임포트
```
댓글 폼 생성
```python
...
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text'] # 필요한 필드는 글을 쓸 곳뿐!
```

## views.py Create 함수 생성
바꿔야 할 코드
```python 
from .models import Post, Comment # Comment 모델 가져오기
```
댓글 생성 코드
```python
# 댓글 생성
def comment_new(request, post_id):
    post = get_object_or_404(Post, pk=post_id) # 해당 포스트의 데이터 가져오기
    if request.method == 'POST':
        form = CommentForm(request.POST) # 폼으로 보낸 데이터 저장
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('/posts/' + str(post.id)) 
    else:
        # 추가가 아니면 그냥 페이지를 보여준다.
        form = CommentForm() # comment form 틀을 가져온다.
        return render(request, 'posts/comment_new.html', {"form":form})
```
## urls.py에 path 등록해주기
path를 등록하여 웹상에서 해당 리소스, 자원 등을 찾을 수 있게 해준다.
```python
    # CREATE(comment_create)
    path('comment_new/<int:post_id>', views.comment_new, name='comment_new'),
```

# 댓글 수정(Update)
## views.py Update 함수 생성
```python
# 댓글 수정
def comment_update(request, comment_id):
    cur_comment = get_object_or_404(Comment, pk = comment_id) # 현재 댓글 내용을 가져오기
    post = cur_comment.post # 현재 포스트 내용을 가져와 준다.

    if request.method == 'POST':
        form = CommentForm(request.POST, instance= cur_comment) # 현재 및 수정된 댓글 주입
        if form.is_valid():
            comment = form.save(commit=False) 
            comment.author = request.user
            comment.save() # 댓글 저장
            return redirect('/posts/' + str(post.id))
    else:
        form = CommentForm(instance=cur_comment)
    return render(request, 'posts/comment_update.html', {'form': form})
```
## urls.py path 추가
```python
    #UPDATE(update)
    path('update/<int:comment_id>', views.comment_update, name='update'),
```

## comment_update.html 생성
```python 
{% extends 'base.html' %}
{% block contents %}
<!--content -->
<div class='container' style="padding-top: 4rem;">
    <form method = 'post' enctype="multipart/form-data">
        {% csrf_token %}
        <table>
            {{form.as_table}}
        </table>
        <br>
        <input class="btn btn-dart" type = "submit" value = "제출하기">
    </form>
</div>
<!-- //content -->
{% endblock %}
```
# 댓글 삭제(Delete)
## view.py 삭제 함수 코드
```python
# 댓글 삭제
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id) # 해당 코멘트 가져오기
    if request.user != comment.author: # 댓글을 달은 유저인지 확인
        return redirect('/posts/'+str(comment.post.id))
    else:
        comment.delete() # 댓글 삭제 메소드
    return redirect('/posts/'+str(comment.post.id))
```
## detail.html 수정, 삭제 버튼 추가
```html
                            <div>
                                <a href="{% url 'update' comment.id %}" class="btn btn-primary">수정</a>
                                <a href="{% url 'delete' comment.id %}" class="btn btn-danger">Delete</a>
                            </div>
```
