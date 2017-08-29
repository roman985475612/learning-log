from django.conf.urls import url

from .views import (
	QuestionList,
	VoteFormView,
	ResultsView,
)

app_name = 'polls'

urlpatterns = [
    url(r'^$', QuestionList.as_view(), name='questions'),
    url(r'^(?P<pk>\d+)/$', VoteFormView.as_view(), name='question'),
    url(r'^(?P<pk>\d+)/results/$', ResultsView.as_view(), name='results'),
]
