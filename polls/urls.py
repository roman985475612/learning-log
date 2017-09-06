from django.conf.urls import url

from .views import (
	QuestionList,
	VoteFormView,
	ResultsView,
    PersonAnswerDetailView,
    MostPopularAnswerDetailView,
)

app_name = 'polls'

urlpatterns = [
    url(r'^$', QuestionList.as_view(), name='questions'),
    url(r'^(?P<pk>\d+)/$', VoteFormView.as_view(), name='question'),
    url(r'^(?P<pk>\d+)/results/$', ResultsView.as_view(), name='results'),
    url(r'^answer/$', PersonAnswerDetailView.as_view(), name='answer'),
    url(r'^popular-answer/$', MostPopularAnswerDetailView.as_view(), name='popular-answer'),
]
