from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^', include('learning_logs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^polls/', include('polls.urls')),
    url(r'^users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
