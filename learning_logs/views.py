from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy

from .models import Topic, Entry, Comment
from .forms import TopicForm, EntryForm, CommentForm


class OwnerVerificationMixins:

    def get_object(self):
        object = super(OwnerVerificationMixins, self).get_object()
        if object.owner != self.request.user:
            raise Http404("You are not the owner")
        return object


class TopicMixins:
    model = Topic


class EntryMixins:
    model = Entry


class CommentMixins:
    model = Comment


class IndexView(ListView):
    queryset = Entry.objects.order_by('-views')[:3]
    context_object_name = 'entries'
    template_name = 'learning_logs/index.html'


class TopicList(TopicMixins, ListView):
    context_object_name = 'topics'


class TopicDetail(TopicMixins, DetailView):
    context_object_name = 'topic'


class EntryDetail(EntryMixins, DetailView):
    context_object_name = 'entry'

    def get_object(self):
        entry = super(EntryDetail, self).get_object()
        entry.views += 1
        entry.save()
        return entry


class TopicCreate(TopicMixins, LoginRequiredMixin, CreateView):
    template_name_suffix = '_create'
    form_class = TopicForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(TopicCreate, self).form_valid(form)


class TopicUpdate(TopicMixins, OwnerVerificationMixins, LoginRequiredMixin, UpdateView):
    form_class = TopicForm
    template_name_suffix = '_update'


class TopicDelete(TopicMixins, OwnerVerificationMixins, LoginRequiredMixin, DeleteView):
    template_name_suffix = '_delete'
    success_url = reverse_lazy('learning_logs:topics')


class EntryCreate(EntryMixins, LoginRequiredMixin, CreateView):
    template_name_suffix = '_create'
    form_class = EntryForm

    def get_context_data(self, **kwargs):
        context = super(EntryCreate, self).get_context_data(**kwargs)
        context['topic'] = get_object_or_404(Topic, slug=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        self.topic = get_object_or_404(Topic, slug=self.kwargs['slug'])
        form.instance.owner = self.request.user
        form.instance.topic = self.topic
        return super(EntryCreate, self).form_valid(form)


class EntryUpdate(EntryMixins, OwnerVerificationMixins, LoginRequiredMixin, UpdateView):
    form_class = EntryForm
    template_name_suffix = '_update'


class EntryDelete(EntryMixins, OwnerVerificationMixins, LoginRequiredMixin, DeleteView):
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse('learning_logs:topic', kwargs={'slug': self.object.topic.slug})


class CommentCreate(CommentMixins, LoginRequiredMixin, CreateView):
    form_class = CommentForm
    template_name_suffix = '_create'

    def get_context_data(self, **kwargs):
        context = super(CommentCreate, self).get_context_data(**kwargs)
        context['entry'] = get_object_or_404(Entry, slug=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        self.entry = get_object_or_404(Entry, slug=self.kwargs['slug'])
        form.instance.owner = self.request.user
        form.instance.entry = self.entry
        return super(CommentCreate, self).form_valid(form)


class CommentUpdate(CommentMixins, OwnerVerificationMixins, LoginRequiredMixin, UpdateView):
    form_class = CommentForm
    template_name_suffix = '_update'


class CommentDelete(CommentMixins, OwnerVerificationMixins, LoginRequiredMixin, DeleteView):
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse('learning_logs:entry', kwargs={'slug': self.object.entry.slug})
