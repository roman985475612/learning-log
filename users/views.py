from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse


class LogoutView(View):
    
    def get(self, request):
        logout(request)
        return redirect('learning_logs:index') 


class RegisterView(View):
    
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST) 
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(
                username=new_user.username,
                password=request.POST['password1']
            )
            login(request, authenticated_user)
            return redirect('learning_logs:index') 

        return render(request, 'users/register.html', {'form': form})
