from django.conf.urls import url

from . import views

app_name = 'learning_logs'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^entry/add/$', views.EntryCreate.as_view(), name='entry_create'),
    url(r'^tags/$', views.TagListView.as_view(), name='tags'),
    url(r'^tag/add/$', views.TagCreateView.as_view(), name='tag_create'),
    url(r'^tag/(?P<slug>[\w-]+)/$',
        views.EntryTagListView.as_view(), name='entry_tag'),

    url(r'^entry/list/newest/$',
        views.EntryNewestListView.as_view(), name='entry_newest'),
    url(r'^entry/list/oldest/$',
        views.EntryOldestListView.as_view(), name='entry_oldest'),
    url(r'^entry/list/commented/$',
        views.EntryMostCommentedListView.as_view(), name='entry_commented'),
    url(r'^entry/list/viewed/$',
        views.EntryPopularListView.as_view(), name='entry_viewed'),
    url(r'^entry/list/likes/$',
        views.EntryLikedListView.as_view(), name='entry_liked'),
    url(r'^entry/list/abc/$', views.EntryListView.as_view(), name='entries'),
    url(r'^entry/(?P<slug>[\w-]+)/$',
        views.EntryDetail.as_view(), name='entry'),
    url(r'^entry/(?P<slug>[\w-]+)/like/$',
        views.EntryLikeRedirectView.as_view(), name='entry_like'),
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
