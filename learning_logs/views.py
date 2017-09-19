from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormMixin, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy

from learning_logs.models import Topic, Tag, Entry, Comment
from users.models import Person

from .forms import TopicForm, TagForm, EntryForm, CommentForm


class OwnerVerificationMixins:

    def get_object(self):
        object = super().get_object()
        if object.owner != self.request.user:
            raise Http404("You are not the owner")
        return object


class IndexView(ListView):
    queryset = Entry.objects.order_by('-views')[:4]
    template_name = 'learning_logs/index.html'


class TopicList(ListView):
    model = Topic
    context_object_name = 'topics'


class TopicDetail(DetailView):
    model = Topic
    context_object_name = 'topic'


class TagListView(ListView):
    model = Tag
    context_object_name = 'tags'


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    template_name_suffix = '_create'
    form_class = TagForm
    success_url = reverse_lazy('learning_logs:index')


class NewestEntryListView(ListView):
    queryset = Entry.objects.order_by('-date_added')[:8]
    template_name = 'learning_logs/newest_entry_list.html'


class MostViewedEntryListView(ListView):
    queryset = Entry.objects.order_by('-views')[:8]
    template_name = 'learning_logs/most_viewed_entry_list.html'


class FilteredTagEntryListView(ListView):
    template_name = 'learning_logs/filtered_tag_entry_list.html'

    def get_queryset(self):
        self.entry = Entry.objects.filter(tag__slug=self.kwargs['slug'])
        return self.entry


class EntryListView(ListView):
    template_name = 'learning_logs/entry_filtered_list.html'

    def get_queryset(self):
        self.query = self.request.GET.get('query')
        if self.query:
            self.entry = Entry.objects.filter(text__icontains=self.query)
        else:
            self.entry = Entry.objects.all()
        return self.entry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query
        return context


class EntryDetail(DetailView):
    model = Entry
    context_object_name = 'entry'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context

    def get_object(self):
        entry = super().get_object()
        entry.views += 1
        entry.save()
        return entry


class TopicCreate(LoginRequiredMixin, CreateView):
    model = Topic
    template_name_suffix = '_create'
    form_class = TopicForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TopicUpdate(OwnerVerificationMixins, LoginRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name_suffix = '_update'


class TopicDelete(OwnerVerificationMixins, LoginRequiredMixin, DeleteView):
    model = Topic
    template_name_suffix = '_delete'
    success_url = reverse_lazy('learning_logs:topics')


class EntryCreate(LoginRequiredMixin, CreateView):
    model = Entry
    template_name_suffix = '_create'
    form_class = EntryForm

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, slug=self.kwargs['slug'])
        return self.topic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = self.get_queryset()
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.topic = self.get_queryset()
        form.save()
        return super().form_valid(form)


class EntryUpdate(OwnerVerificationMixins, LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name_suffix = '_update'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EntryDelete(OwnerVerificationMixins, LoginRequiredMixin, DeleteView):
    model = Entry
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse('learning_logs:topic', kwargs={'slug': self.object.topic.slug})


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name_suffix = '_create'

    def get_queryset(self):
        self.entry = get_object_or_404(Entry, slug=self.kwargs['slug'])
        return self.entry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entry'] = self.get_queryset()
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.entry = self.get_queryset()
        return super().form_valid(form)


class CommentUpdate(OwnerVerificationMixins, LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name_suffix = '_update'


class CommentDelete(OwnerVerificationMixins, LoginRequiredMixin, DeleteView):
    model = Comment
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse('learning_logs:entry', kwargs={'slug': self.object.entry.slug})
