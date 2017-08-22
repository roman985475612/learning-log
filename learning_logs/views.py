from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


class IndexView(TemplateView):
    template_name = 'learning_logs/index.html'


class TopicList(ListView):
    queryset = Topic.objects.order_by('title')
    template_name = 'learning_logs/topics.html' 
    context_object_name = 'topics'


class TopicDetail(ListView):

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, slug=self.kwargs['slug'])
        return Entry.objects.filter(topic=self.topic).order_by('-date_added')
    
    def get_context_data(self, **kwargs):
        context = super(TopicDetail, self).get_context_data(**kwargs)
        context['topic'] = self.topic
        return context

    template_name = 'learning_logs/topic.html'
    context_object_name = 'entries'


class EntryDetail(ListView):
    def get_queryset(self):
        self.entry = get_object_or_404(Entry, slug=self.kwargs['slug'])
        return self.entry

    context_object_name = 'entry'
    template_name = 'learning_logs/entry.html'
    

class TopicCreate(CreateView):
    form_class = TopicForm
    template_name = 'learning_logs/topic_create.html'
    success_url = reverse_lazy('learning_logs:topics')


class TopicUpdate(UpdateView):
    model = Topic
    form_class = TopicForm
    context_object_name = 'topic'
    template_name = 'learning_logs/topic_update.html'
    success_url = reverse_lazy('learning_logs:topics')


class TopicDelete(DeleteView):
    model = Topic
    success_url = reverse_lazy('learning_logs:topics')
    

class EntryCreate(View):
    form_class = EntryForm
    template_name = 'learning_logs/entry_create.html'

    def get(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, slug=self.kwargs['slug'])
        form = self.form_class()
        return render(request, self.template_name, {'topic': topic, 'form': form})

    def post(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, slug=self.kwargs['slug'])
        form = self.form_class(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic.slug)

        return render(request, self.template_name, {'topic': topic, 'form': form})


class EntryUpdate(View):
    form_class = EntryForm
    template_name = 'learning_logs/entry_update.html'

    def get(self, request, *args, **kwargs):
        entry = get_object_or_404(Entry, slug=self.kwargs['slug'])
        topic = entry.topic
        form = self.form_class(instance=entry)
        return render(request, self.template_name, {
            'entry': entry,
            'topic': topic,
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        entry = get_object_or_404(Entry, slug=self.kwargs['slug'])
        topic = entry.topic
        form = self.form_class(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:entry', entry.slug)
        return render(request, self.template_name, {
            'entry': entry,
            'topic': topic,
            'form': form,
        })


class EntryDelete(View):
    pass
