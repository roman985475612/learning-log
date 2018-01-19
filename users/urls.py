from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    PersonDetailView,
    PersonUpdateView
)

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', PersonDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/update/', PersonUpdateView.as_view(), name='profile_update'),
]
