from django.urls import path

from .views import (
    IndexView,
    TagListView,
    TagCreateView,
    EntryListView,
    EntryNewestListView,
    EntryTopListView,
    EntryTagListView,
    EntryCreateView,
    EntryDetailView,
    EntryLikeView,
    EntryUpdateView,
    EntryDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView
)

app_name = 'learning_logs'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('tags/', TagListView.as_view(), name='tags'),
    path('tag/add/', TagCreateView.as_view(), name='tag_create'),
    path('entries/', EntryListView.as_view(), name='entries'),
    path('new/', EntryNewestListView.as_view(), name='newest'),
    path('top/', EntryTopListView.as_view(), name='top'),
    path('tag/<slug:slug>/', EntryTagListView.as_view(), name='tag'),
    path('entry/add/', EntryCreateView.as_view(), name='entry_create'),
    path('entry/<slug:slug>/', EntryDetailView.as_view(), name='entry'),
    path('entry/<slug:slug>/like/', EntryLikeView.as_view(), name='entry_like'),
    path('entry/<slug:slug>/update/', EntryUpdateView.as_view(), name='entry_update'),
    path('entry/<int:pk>/delete/', EntryDeleteView.as_view(), name='entry_delete'),
    path('entry/<slug:slug>/comment/add/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]
