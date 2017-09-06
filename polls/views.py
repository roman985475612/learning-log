from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy


from .models import Question, Choice, Answer
from .forms import VoteForm


class QuestionList(LoginRequiredMixin, ListView):
    model = Question
    context_object_name = 'question_list'


class VoteFormView(LoginRequiredMixin, FormView):
    form_class = VoteForm
    template_name = 'polls/question_detail.html'

    def get_queryset(self):
        self.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        return self.question

    def get_context_data(self, **kwargs):
        context = super(VoteFormView, self).get_context_data(**kwargs)
        context['question'] = self.get_queryset()
        return context

    def get_form_kwargs(self):
        kwargs = super(VoteFormView, self).get_form_kwargs()
        kwargs['question'] = self.get_queryset()
        return kwargs

    def form_valid(self, form):
        self.selected_choice = get_object_or_404(Choice, pk=self.request.POST['vote'])
        self.selected_choice.votes += 1
        self.selected_choice.save()
        
        current_answer = Answer.objects.create(
            owner=self.request.user,
            question=self.get_queryset(),
            choice=self.selected_choice
        )
        current_answer.save()
        return super(VoteFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('polls:results', kwargs={'pk': self.kwargs['pk']})


class ResultsView(LoginRequiredMixin, DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'polls/results.html'


class PersonAnswerDetailView(LoginRequiredMixin, ListView):
    template_name = 'polls/person_answer_detail.html'
    context_object_name = 'answers'

    def get_queryset(self):
        self.last_answers = []

        answers = Answer.objects.filter(owner=self.request.user)
        questions = answers.values_list('question__text', flat=True).distinct()
        
        for question in questions:
            self.last_answers.append(answers.filter(question__text=question).order_by('date_added').last())

        return self.last_answers
