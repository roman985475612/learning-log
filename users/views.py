from django.contrib.auth import logout
from django.views.generic import View
from django.shortcuts import render, redirect


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('learning_logs:index') 
