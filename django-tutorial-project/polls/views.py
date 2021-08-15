from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from . models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Возвращает последние 5 опубликованных вопроса"""
        return Question.objects.order_by('-publication_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(
        request,
        template_name='polls/detail.html',
        context={'question': question}
    )


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(
        request,
        template_name='polls/results.html',
        context={'question': question}
    )


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            template_name='polls/detail.html',
            context={'question': question,
                     'error_message': "You didn't select a choice.",
            }
        )
    else:
        # При сохранении возникает состояние гонки.
        # Решение: https://docs.djangoproject.com/en/3.2/ref/models/expressions/#avoiding-race-conditions-using-f
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

