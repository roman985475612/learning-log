from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormMixin, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy

from learning_logs.models import Tag, Entry, Comment
from users.models import Person

from .forms import TagForm, EntryForm, CommentForm


class OwnerVerificationMixins:

    def get_object(self):
        object = super().get_object()
        if object.owner != self.request.user:
            raise Http404("You are not the owner")
        return object


class IndexView(ListView):
    queryset = Entry.objects.order_by('-views')[:4]
    template_name = 'learning_logs/index.html'


class TagListView(ListView):
    model = Tag
    context_object_name = 'tags'


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    template_name_suffix = '_create'
    form_class = TagForm
    success_url = reverse_lazy('learning_logs:index')


class EntryListView(ListView):
    paginate_by = 3

    def get_queryset(self):
        self.entry_list = Entry.objects.all()

        self.query = self.request.GET.get('query')
        if self.query:
            self.entry_list = self.entry_list.filter(
                Q(title__icontains=self.query)|
                Q(text__icontains=self.query)
            )

        self.tag_query = self.request.GET.get('tag_query')
        if self.tag_query:
            self.entry_list = self.entry_list.filter(tag__slug=self.tag_query)

        self.sort_by = self.request.GET.get('sort_by')
        if self.sort_by:
            self.entry_list = self.entry_list.order_by(self.sort_by)

        return self.entry_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['query'] = self.query
        context['tag_query'] = self.tag_query
        context['sort_by'] = self.sort_by
        return context


class EntryDetail(DetailView):
    model = Entry
    context_object_name = 'entry'
    form_class = CommentForm

    def get_object(self):
        self.entry = super().get_object()
        self.entry.views += 1
        self.entry.save()
        return self.entry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        context['avatar'] = self.get_object().owner.person.image
        context['avatar_url'] = context['avatar'].url
        context['tags'] = self.get_object().tag.all()
        context['comments'] = self.get_object().comment_set.all()
        return context


class EntryLikeRedirectView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        entry = get_object_or_404(Entry, slug=self.kwargs['slug'])
        entry.likes += 1
        entry.save()
        return reverse('learning_logs:entry', kwargs={'slug': self.kwargs['slug']})


class EntryCreate(LoginRequiredMixin, CreateView):
    model = Entry
    template_name_suffix = '_create'
    form_class = EntryForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
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
        entry = self.get_queryset()
        form.instance.entry = entry
        entry.comments += 1
        entry.save()
        return super().form_valid(form)


class CommentUpdate(OwnerVerificationMixins, LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name_suffix = '_update'


class CommentDelete(OwnerVerificationMixins, LoginRequiredMixin, DeleteView):
    model = Comment
    template_name_suffix = '_delete'

    def delete(self, request, *args, **kwargs):
        self.entry = self.get_object().entry
        self.entry.comments -= 1
        self.entry.save()
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('learning_logs:entry', kwargs={'slug': self.object.entry.slug})
