from django.conf.urls import url

from .views import (
	QuestionList,
	QuestionDetail,
	ResultsView,
	vote,
)

app_name = 'polls'

urlpatterns = [
    url(r'^$', QuestionList.as_view(), name='questions'),
    url(r'^(?P<pk>\d+)/$', QuestionDetail.as_view(), name='question'),
    url(r'^(?P<pk>\d+)/vote/$', vote, name='vote'),
    url(r'^(?P<pk>\d+)/results/$', ResultsView.as_view(), name='results'),
]
