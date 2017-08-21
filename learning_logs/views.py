from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


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
        return Entry.objects.filter(topic=self.topic).order_by('-date_added')
    
    def get_context_data(self, **kwargs):
        context = super(TopicDetail, self).get_context_data(**kwargs)
        context['topic'] = self.topic
        return context

    context_object_name = 'entries'


class EntryDetail(ListView):
    def get_queryset(self):
        self.entry = get_object_or_404(Entry, slug=self.kwargs['entry_slug'])
        return self.entry

    context_object_name = 'entry'
    template_name = 'learning_logs/entry.html'
    

class TopicCreate(CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'learning_logs/topic_create.html'
    success_url = reverse_lazy('learning_logs:topics')


class TopicUpdate(UpdateView):
    model = Topic
    slug_url_kwarg = 'topic_slug'
    form_class = TopicForm
    context_object_name = 'topic'
    template_name = 'learning_logs/topic_update.html'
    success_url = reverse_lazy('learning_logs:topics')


class TopicDelete(DeleteView):
    model = Topic
    slug_url_kwarg = 'topic_slug'
    success_url = reverse_lazy('learning_logs:topics')
    

class EntryCreate(CreateView):
    pass
