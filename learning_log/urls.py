from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('learning_logs.urls')),
    url(r'^users/', include('users.urls')),
]
