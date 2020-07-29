from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import posts.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', posts.views.index, name="index"),

    path('accounts/', include('accounts.urls')),
    path('posts/', include('posts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
