from django.conf.urls import url

from . import views

app_name = 'learning_logs'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'), 
    url(r'^topics/$', views.TopicList.as_view(), name='topics'),
]
