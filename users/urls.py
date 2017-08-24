from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

app_name = 'users'

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
]
