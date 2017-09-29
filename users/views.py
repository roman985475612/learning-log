from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy

from .models import Person
from .forms import PersonForm


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('learning_logs:index')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.success_url)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('learning_logs:index')


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('learning_logs:index')

    def form_valid(self, form):
        form.save()
        login(self.request, authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        ))
        return redirect(self.success_url)


class PersonMixins(View):
    def get_person(self, request, *args, **kwargs):
        self.person = Person.objects.get(owner=self.request.user)
        return self.person

    def dispatch(self, request, *args, **kwargs):
        try:
            person = self.get_person(request)
        except Person.DoesNotExist:
            return redirect('users:profile_create')
        return super(PersonMixins, self).dispatch(request)


class PersonDetailView(LoginRequiredMixin, PersonMixins, TemplateView):
    template_name = 'users/person_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['person'] = self.get_person(self.request)
        context['entry_list'] = context['person'].owner.entry.all()
        context['comment_list'] = context['person'].owner.comment.order_by('entry', '-date_added')
        return context


class PersonCreateView(LoginRequiredMixin, CreateView):
    model = Person
    form_class = PersonForm
    template_name_suffix = '_create'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PersonCreateView, self).form_valid(form)


class PersonUpdateView(LoginRequiredMixin, PersonMixins, FormView):
    form_class = PersonForm
    template_name = 'users/person_update.html'
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        person = self.get_person(self.request)
        context['form'] = self.form_class(instance=person)
        return context

    def form_valid(self, form):
        person = Person.objects.get(owner=self.request.user)
        form = self.form_class(instance=person, data=self.request.POST)
        form.save()
        return super().form_valid(form)


class PersonDeleteView(LoginRequiredMixin, PersonMixins, TemplateView):
    template_name = 'users/person_delete.html'

    def post(self, request, *args, **kwargs):
        person = self.get_person(request)
        person.delete()
        return redirect('learning_logs:index')
