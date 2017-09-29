from django.conf.urls import url

from . import views

app_name = 'users'

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^profile/(?P<pk>\d+)/$', views.PersonDetailView.as_view(), name='profile'),
    url(r'^profile/(?P<pk>\d+)/create/$', views.PersonCreateView.as_view(), name='profile_create'),
    url(r'^profile/(?P<pk>\d+)/update/$', views.PersonUpdateView.as_view(), name='profile_update'),
]
