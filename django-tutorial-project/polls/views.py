from django.shortcuts import get_object_or_404, render

from . models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-publication_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, template_name='polls/index.html', context=context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(
        request,
        template_name='polls/index.html',
        context={'question': question}
    )


def results(request, question_id):
    pass
    # return HttpResponse(f"You're looking at the results of question {question_id}")


def vote(request, question_id):
    pass
    # return HttpResponse(f"You're voting on {question_id}")

