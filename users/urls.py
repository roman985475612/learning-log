from django.conf.urls import url

from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    PersonDetailView,
    PersonCreateView,
    PersonUpdateView,
    PersonDeleteView,
)

app_name = 'users'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^profile/$', PersonDetailView.as_view(), name='profile'),
    url(r'^profile/create/$', PersonCreateView.as_view(), name='profile_create'),
    url(r'^profile/update/$', PersonUpdateView.as_view(), name='profile_update'),
    url(r'^profile/delete/$', PersonDeleteView.as_view(), name='profile_delete'),
]
