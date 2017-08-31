from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy


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
