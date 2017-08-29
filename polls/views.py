from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy


from .models import Question, Choice
from .forms import VoteForm


class QuestionList(ListView):
    model = Question
    context_object_name = 'question_list'


class VoteFormView(FormView):
    form_class = VoteForm
    template_name = 'polls/question_detail.html'

    def get_queryset(self):
        self.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        return self.question

    def form_valid(self, form):
        self.selected_choice = get_object_or_404(Choice, pk=self.request.POST['vote'])
        self.selected_choice.votes += 1
        self.selected_choice.save()
        return super(VoteFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('polls:results', kwargs={'pk': self.kwargs['pk']})


class ResultsView(DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'polls/results.html'
