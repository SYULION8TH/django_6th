from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # post app
    # CREATE (new, create)
    path('new/', views.new, name="new"),
    path('create/', views.create, name="create"),
    # READ(detail)
    path('<int:post_id>/', views.detail, name='detail'),
    # 댓글 생성(comment_new)
    # 댓글 수정(comment_update)
    # 댓글 삭제(comment_delete)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

