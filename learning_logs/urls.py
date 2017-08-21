from django.conf.urls import url

from . import views

app_name = 'learning_logs'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'), 
    url(r'^topic/list/$', views.TopicList.as_view(), name='topics'),
    url(r'^topic/create/$', views.TopicCreate.as_view(), name='topic_create'),
    url(r'^topic/(?P<topic_slug>[\w-]+)/update/$', views.TopicUpdate.as_view(), name='topic_update'),
    url(r'^topic/(?P<topic_slug>[\w-]+)/delete/$', views.TopicDelete.as_view(), name='topic_delete'),
    url(r'^topic/(?P<topic_slug>[\w-]+)/entry/list/$', views.TopicDetail.as_view(), name='topic'),
    url(r'^topic/(?P<topic_slug>[\w-]+)/entry/create/$', views.EntryCreate.as_view(), name='entry_create'),
    url(r'^topic/(?P<topic_slug>[\w-]+)/entry/(?P<entry_slug>[\w-]+)/$',
        views.EntryDetail.as_view(), name='entry'),
]
