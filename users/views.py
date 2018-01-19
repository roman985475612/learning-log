from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
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
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log In'
        return context


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('learning_logs:index')


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('learning_logs:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

    def form_valid(self, form):
        form.save()
        login(self.request, authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        ))
        # Create Person model
        obj = Person.objects.get_or_create(owner=self.request.user)[0]
        obj.save()
        # Display message
        msg = 'Account {} was registered successfully'.format(self.request.user.username)
        messages.success(self.request, msg)
        return super().form_valid(form)


class PersonDetailView(LoginRequiredMixin, DetailView):
    model = Person
    template_name = 'users/person_detail.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile: {}'.format(self.request.user.username)
        return context


class PersonUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Person
    form_class = PersonForm
    success_message = "Your profile was updated successfully"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Updata: {}'.format(self.request.user.username)
        return context

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.object.pk})


class PersonDeleteView():
    pass
