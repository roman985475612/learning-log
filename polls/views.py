from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Question, Choice
from .forms import VoteForm


class QuestionList(ListView):
    model = Question
    context_object_name = 'question_list'


# class QuestionDetail(DetailView):
#     model = Question
#     context_object_name = 'question'

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            selected_choice = Choice.objects.get(pk=request.POST['vote'])
            selected_choice.votes += 1
            selected_choice.save()
            return redirect(reverse('polls:results', args=[question.id]))
    else:
        form = VoteForm(form_kwargs={'question': question})

    return render(request, 'polls/question_detail.html', {
        'question': question,
        'form': form,
    })


class ResultsView(DetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'polls/results.html'
