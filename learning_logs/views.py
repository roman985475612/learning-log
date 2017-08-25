from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy

from .models import Topic, Entry, Comment
from .forms import TopicForm, EntryForm, CommentForm


class IndexView(TemplateView):
    template_name = 'learning_logs/index.html'


class TopicList(ListView):
    model = Topic


class TopicDetail(DetailView):
    model = Topic


class EntryDetail(ListView):
    template_name = 'learning_logs/entry_detail.html'

    def get_queryset(self):
        self.entry = get_object_or_404(Entry, slug=self.kwargs['slug'])
        return Comment.objects.filter(entry=self.entry)

    def get_context_data(self, *args, **kwargs):
        context = super(EntryDetail, self).get_context_data(*args, **kwargs)
        context['entry'] = self.entry
        return context
    

class TopicCreate(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'learning_logs/topic_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(TopicCreate, self).form_valid(form)


class TopicUpdate(LoginRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'learning_logs/topic_update.html'

    def get_object(self):
        object = super(TopicUpdate, self).get_object()
        if object.owner != self.request.user:
            raise Http404("You are not the owner")
        return object


class TopicDelete(LoginRequiredMixin, DeleteView):
    model = Topic
    success_url = reverse_lazy('learning_logs:topics')

    def get_object(self):
        object = super(TopicDelete, self).get_object()
        if object.owner != self.request.user:
            raise Http404("You are not the owner")
        return object


class EntryCreate(LoginRequiredMixin, FormView):
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
            new_entry.owner = request.user
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic.slug)

        return render(request, self.template_name, {'topic': topic, 'form': form})


class EntryUpdate(LoginRequiredMixin, FormView):
    form_class = EntryForm
    template_name = 'learning_logs/entry_update.html'

    def get(self, request, *args, **kwargs):
        entry = get_object_or_404(Entry, slug=self.kwargs['slug'])
        if entry.owner != self.request.user:
            raise Http404("You are not the owner")
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


class EntryDelete(LoginRequiredMixin, DeleteView):
    model = Entry
    
    def get_object(self):
        object = super(EntryDelete, self).get_object()
        if object.owner != self.request.user:
            raise Http404("You are not owner")
        return object

    def get_success_url(self):
        return reverse('learning_logs:topic', kwargs={'slug': self.object.topic.slug})


class CommentCreate(LoginRequiredMixin, CreateView):
    template_name = 'learning_logs/comment_create.html'
    form_class = CommentForm

    def form_valid(self, form):
        self.entry = get_object_or_404(Entry, slug=self.kwargs['slug'])
        form.instance.owner = self.request.user
        form.instance.entry = self.entry
        return super(CommentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('learning_logs:entry', kwargs={'slug': self.object.entry.slug})
