from django.conf.urls import url

from . import views

app_name = 'learning_logs'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'), 
    url(r'^topics/$', views.TopicList.as_view(), name='topics'),
    url(r'^topic/(?P<topic_slug>[\w-]+)/$', views.TopicDetail.as_view(), name='topic'),
    url(r'^topic/(?P<topic_slug>[\w-]+)/entry/(?P<entry_slug>[\w-]+)/$',
        views.EntryDetail.as_view(), name='entry'),
]
