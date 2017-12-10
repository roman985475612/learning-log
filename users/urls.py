from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.login, {'template_name': 'users/login.html'}, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', views.PersonDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/create/', views.PersonCreateView.as_view(), name='profile_create'),
    path('profile/<int:pk>/update/', views.PersonUpdateView.as_view(), name='profile_update'),
]
