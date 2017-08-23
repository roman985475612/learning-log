from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'learning_logs'

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='learning_logs/index.html'), name='index'), 
    url(r'^topics/$', views.TopicList.as_view(), name='topics'),
    url(r'^topic-add/$', views.TopicCreate.as_view(), name='topic_create'),
    url(r'^topic/(?P<slug>[\w-]+)/update/$', views.TopicUpdate.as_view(), name='topic_update'),
    url(r'^topic/(?P<slug>[\w-]+)/delete/$', views.TopicDelete.as_view(), name='topic_delete'),
    url(r'^topic/(?P<slug>[\w-]+)/$', views.TopicDetail.as_view(), name='topic'),
    url(r'^topic/(?P<slug>[\w-]+)/entry-add/$', views.EntryCreate.as_view(), name='entry_create'),
    url(r'^entry/(?P<slug>[\w-]+)/$', views.EntryDetail.as_view(), name='entry'),
    url(r'^entry/(?P<slug>[\w-]+)/update/$', views.EntryUpdate.as_view(), name='entry_update'),
    url(r'^entry/(?P<slug>[\w-]+)/delete/$', views.EntryDelete.as_view(), name='entry_delete'),
]
