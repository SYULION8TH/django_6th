from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment # Comment 모델 가져오기
from .forms import BlogPost,CommentForm
from django.core.paginator import Paginator # 장고 내장 페이지네이션 기능을 가져온다.
from django.utils import timezone

# CREATE(new, create)
def new(request):
    if request.method == 'POST': # 요청 메소드가 POST일 때
        form = BlogPost(request.POST, request.FILES) # 폼에 데이터와 파일 넣기
        if form.is_valid(): # validation 유효성 검사
            post = form.save(commit=False) # post에 담기 commit이 true냐 false냐는 지금 바로 저장하냐 나중에 저장하냐 차이, 나중에 저장하면 post.save()메소드를 이용하여 저장해주어야함.
            post.created_at = timezone.now() # 만들어진 시간 넣기
            post.save() # 데이터 저장
            return redirect('/posts/' + str(post.id)) 
    else: # POST가 아닐때
        form = BlogPost()
        return render(request, 'posts/new.html', {'form':form})

def create(request):
    post = Post()
    post.title = request.GET['title']
    post.body = request.GET['body']
    post.created_at = timezone.datetime.now()
    post.save()

    return redirect('/post/' + str(post.id))

# READ(index, detail)
def index(request):
    posts = Post.objects.all().order_by('id') # posts는 게시글이 담긴 배열
    paginator = Paginator(posts, 3) # 페이지네이터 함수 사용
    page_number = request.GET.get("page") # 페이지 넘버 가져오기
    page_posts = paginator.get_page(page_number)
    return render(request, "posts/index.html", {"posts":page_posts})

def detail(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    return render(request, 'posts/detail.html', {"post":post})

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
# 댓글 삭제
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id) # 해당 코멘트 가져오기
    if request.user != comment.author: # 댓글을 달은 유저인지 확인
        return redirect('/posts/'+str(comment.post.id))
    else:
        comment.delete() # 댓글 삭제 메소드
    return redirect('/posts/'+str(comment.post.id))