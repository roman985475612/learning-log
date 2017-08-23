from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, RedirectView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


class TopicList(ListView):
    model = Topic


class TopicDetail(DetailView):
    model = Topic


class EntryDetail(DetailView):
    model = Entry
    

class TopicCreate(CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'learning_logs/topic_create.html'


class TopicUpdate(UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'learning_logs/topic_update.html'


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


class EntryDelete(DeleteView):
    model = Entry
    
    def get_success_url(self):
        return reverse('learning_logs:topic', kwargs={'slug': self.object.topic.slug})
