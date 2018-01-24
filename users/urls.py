from django.urls import path

from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    ProfileDetailView,
    ProfileUpdateView,
    ProfileDeleteView
)

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('delete/', ProfileDeleteView.as_view(), name='profile_delete'),
]
