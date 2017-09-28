from django.conf.urls import url

from . import views

app_name = 'learning_logs'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^tags/$', views.TagListView.as_view(), name='tags'),
    url(r'^tag/add/$', views.TagCreateView.as_view(), name='tag_create'),

    url(r'^entries/$', views.EntryListView.as_view(), name='entries'),
    url(r'^new/$', views.EntryNewestListView.as_view(), name='newest'),
    url(r'^top/$', views.EntryTopListView.as_view(), name='top'),
    url(r'^tag/(?P<tag_slug>[\w-]+)/$', views.EntryTagListView.as_view(), name='tag'),
    url(r'^owner/(?P<owner>[\w-]+)/$', views.EntryOwnerListView.as_view(), name='owner'),
    url(r'^entry/add/$', views.EntryCreate.as_view(), name='entry_create'),
    url(r'^entry/(?P<slug>[\w-]+)/$',
        views.EntryDetailView.as_view(), name='entry'),
    url(r'^entry/(?P<slug>[\w-]+)/like/$',
        views.EntryLikeView.as_view(), name='entry_like'),
    url(r'^entry/(?P<slug>[\w-]+)/update/$',
        views.EntryUpdate.as_view(), name='entry_update'),
    url(r'^entry/(?P<slug>[\w-]+)/delete/$',
        views.EntryDelete.as_view(), name='entry_delete'),
    url(r'^entry/(?P<slug>[\w-]+)/comment/add/$',
        views.CommentCreate.as_view(), name='comment_create'),

    url(r'^comment/(?P<pk>\d+)/update/$',
        views.CommentUpdate.as_view(), name='comment_update'),
    url(r'^comment/(?P<pk>\d+)/delete/$',
        views.CommentDelete.as_view(), name='comment_delete'),
]
