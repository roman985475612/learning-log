from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy

from .models import Person
from .forms import PersonForm


class OwnerVerificationMixins:

    def get_object(self):
        object = super().get_object()
        if object.owner != self.request.user:
            raise Http404("You are not the owner")
        return object


#class LoginView(FormView):
#    template_name = 'users/login.html'
#    form_class = AuthenticationForm
#    success_url = reverse_lazy('learning_logs:index')
#
#    def form_valid(self, form):
#        login(self.request, form.get_user())
#        return redirect(self.success_url)


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
        obj = Person.objects.get_or_create(owner=self.request.user)[0]
        obj.save()
        return redirect(self.success_url)


class PersonDetailView(LoginRequiredMixin, DetailView):
    model = Person
    template_name = 'users/person_detail.html'
    context_object_name = 'person'


class PersonCreateView(LoginRequiredMixin, OwnerVerificationMixins, CreateView):
    model = Person
    form_class = PersonForm
    template_name_suffix = '_create'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PersonUpdateView(LoginRequiredMixin, OwnerVerificationMixins, UpdateView):
    model = Person
    form_class = PersonForm
    template_name_suffix = '_update'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.object.pk})
