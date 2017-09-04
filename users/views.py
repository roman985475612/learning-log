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
        new_user = form.save()
        authenticated_user = authenticate(
            username=new_user.username,
            password=self.request.POST['password1']
        )
        login(self.request, authenticated_user)
        return redirect(self.success_url) 


class PersonMixins(View):
    def get_object(self, request, *args, **kwargs):
        self.person = Person.objects.get(owner=self.request.user)
        return self.person

    def dispatch(self, request, *args, **kwargs):
        try:
            person = self.get_object(request)
        except Person.DoesNotExist:
            return redirect('users:profile_create')
        return super(PersonMixins, self).dispatch(request)


class PersonDetailView(PersonMixins, LoginRequiredMixin, TemplateView):
    template_name = 'users/person_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        context['person'] = self.get_object(self.request)
        return context


class PersonCreateView(LoginRequiredMixin, CreateView):
    model = Person
    form_class = PersonForm
    template_name_suffix = '_create'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PersonCreateView, self).form_valid(form)


class PersonUpdateView(PersonMixins, LoginRequiredMixin, View):
    form_class = PersonForm
    template_name = 'users/person_update.html'

    def get(self, request, *args, **kwargs):
        person = self.get_object(request)
        form = self.form_class(instance=person) 
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        person = self.get_object(request)
        form = self.form_class(instance=person, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:profile')

        return render(request, self.template_name, {'form': form})


class PersonDeleteView(PersonMixins, LoginRequiredMixin, View):
    template_name = 'users/person_delete.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        person = self.get_object(request)
        person.delete()   
        return redirect('learning_logs:index')
