from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import RedirectView, TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormMixin, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy

from learning_logs.models import Tag, Entry, Comment, LogLikedEntries, LogViewedEntries
from users.models import Person

from .forms import TagForm, EntryForm, CommentForm


class MyUserPassesTestMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        owner = self.get_queryset()[0].owner
        return self.request.user == owner


class IndexView(ListView):
    queryset = Entry.objects.all()[:3]
    context_object_name = 'entries'
    template_name = 'learning_logs/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class TagListView(ListView):
    model = Tag
    context_object_name = 'tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tags'
        return context


class TagCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy('learning_logs:tags')
    success_message = "%(title)s was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add new tag'
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            title = self.object.title
        )


class EntryListView(ListView):
    paginate_by = 1

    def get_queryset(self):
        self.entry_list = Entry.objects.all()
        self.question = self.request.GET.get('q')
        if self.question:
            self.entry_list = self.entry_list.filter(
                Q(title__icontains=self.question)|
                Q(text__icontains=self.question)
            ).order_by('-date_added')

        return self.entry_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.question:
            context['last_question'] = '?q=%s' % self.question
        
        context['q'] = self.question
        context['title'] = 'Articles'
        return context


class EntryNewestListView(ListView):
    paginate_by = 1
    queryset = Entry.objects.order_by('-date_added')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Articles'
        return context


class EntryTopListView(ListView):
    paginate_by = 1
    queryset = Entry.objects.order_by('-likes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Top Articles'
        return context
    

class EntryTagListView(ListView):
    paginate_by = 1

    def get_queryset(self):
        self.entry_list = Entry.objects.filter(tag__slug=self.kwargs['slug'])
        return self.entry_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tag: {}'.format(self.kwargs['slug'].title()) 
        return context


class EntryDetailView(DetailView):
    model = Entry
    context_object_name = 'entry'
    form_class = CommentForm

    def dispatch(self, *args, **kwargs):
        self.entry = get_object_or_404(Entry, slug=self.kwargs['slug'])
        self.remote_addr = self.request.META['REMOTE_ADDR']
        obj, created = LogViewedEntries.objects.get_or_create(
            entry=self.entry,
            remote_addr=self.remote_addr
        )
        if created:
            self.entry.views += 1
            self.entry.save()
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        context['tags'] = self.get_object().tag.all()
        context['comments'] = self.get_object().comment_set.all()
        context['title'] = self.get_object().title
        return context


class EntryLikeView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        self.entry = get_object_or_404(Entry, slug=self.kwargs['slug'])
        obj = LogLikedEntries.objects.get_or_create(
            owner=self.request.user,
            entry=self.entry
        )[0]
        if not obj.is_liked:
            obj.is_liked = True
            self.entry.likes += 1
            messages.success(self.request, "Added to Liked entry")
        else:
            obj.is_liked = False
            self.entry.likes -= 1
            messages.success(self.request, "Revoke to Liked entry")

        obj.save()
        self.entry.save()
        return reverse('learning_logs:entry', kwargs={'slug': self.kwargs['slug']})


class EntryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Entry
    form_class = EntryForm
    success_message = "%(title)s was created successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            title = self.object.title,
        )

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add article'
        return context


class EntryUpdateView(MyUserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    success_message = "%(title)s was updated successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            title = self.object.title,
        )

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update article'
        return context


class EntryDeleteView(UserPassesTestMixin, RedirectView):

    def get_queryset(self):
        return get_object_or_404(Entry, pk=self.kwargs['pk'])

    def test_func(self):
        return self.request.user == self.get_queryset().owner

    def post(self, request, *args, **kwargs):
        self.get_queryset().delete()
        messages.success(self.request, 'Entry was deleted successfully')
        return super().post(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('users:profile')


class CommentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    success_message = "Comment was created successfully"

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


class CommentUpdateView(MyUserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    success_message = "Comment was updated successfully"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Updata comment'
        return context


class CommentDeleteView(UserPassesTestMixin, RedirectView):

    # Get comment for deleting
    def get_comment(self):
        return get_object_or_404(Comment, pk=self.kwargs['pk'])
    
    # Check comment owner
    def test_func(self):
        return self.request.user == self.get_comment().owner
    
    # Deleting comment
    def post(self, request, *args, **kwargs):
        entry = self.get_comment().entry
        entry.comments -= 1
        entry.save()
        self.get_comment().delete()
        messages.success(self.request, 'Comment was deleted successfully')
        return super().post(request, *args, **kwargs)

    # Redirect to profile
    def get_redirect_url(self, *args, **kwargs):
        return reverse('users:profile')
