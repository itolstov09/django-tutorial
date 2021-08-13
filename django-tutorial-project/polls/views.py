from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Функция index из приложения polls")


def detail(request, question_id):
    return HttpResponse(f"You're looking at question {question_id}")


def results(request, question_id):
    return HttpResponse(f"You're looking at the results of question {question_id}")


def vote(request, question_id):
    return HttpResponse(f"You're voting on {question_id}")

