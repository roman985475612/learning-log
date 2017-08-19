from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .models import Topic, Entry

class IndexView(TemplateView):
    template_name = 'learning_logs/index.html'


class TopicList(ListView):
    model = Topic
    template_name = 'learning_logs/topics.html' 
    context_object_name = 'topics'
