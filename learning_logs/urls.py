from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'learning_logs'

urlpatterns = [
    path('', TemplateView.as_view(template_name='learning_logs/index.html'), name='index'),
    path('tags/', views.TagListView.as_view(), name='tags'),
    path('tag/add/', views.TagCreateView.as_view(), name='tag_create'),
    path('entries/', views.EntryListView.as_view(), name='entries'),
    path('new/', views.EntryNewestListView.as_view(), name='newest'),
    path('top/', views.EntryTopListView.as_view(), name='top'),
    path('tag/<slug:tag_slug>/', views.EntryTagListView.as_view(), name='tag'),
    path('entry/add/', views.EntryCreate.as_view(), name='entry_create'),
    path('entry/<slug:slug>/', views.EntryDetailView.as_view(), name='entry'),
    path('entry/<slug:slug>/like/', views.EntryLikeView.as_view(), name='entry_like'),
    path('entry/<slug:slug>/update/', views.EntryUpdate.as_view(), name='entry_update'),
    path('entry/<slug:slug>/delete/', views.EntryDelete.as_view(), name='entry_delete'),
    path('entry/<slug:slug>/comment/add/', views.CommentCreate.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),
]
