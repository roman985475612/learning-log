from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from .models import Topic, Entry

class IndexView(TemplateView):
    template_name = 'learning_logs/index.html'


class TopicList(ListView):
    model = Topic
    template_name = 'learning_logs/topics.html' 
    context_object_name = 'topics'


class TopicDetail(ListView):

    template_name = 'learning_logs/topic.html'
    
    def get_queryset(self):
        self.topic = get_object_or_404(Topic, slug=self.kwargs['topic_slug'])
        return Entry.objects.filter(topic=self.topic)
    
    def get_context_data(self, **kwargs):
        context = super(TopicDetail, self).get_context_data(**kwargs)
        context['topic'] = self.topic
        return context

    context_object_name = 'entries'
