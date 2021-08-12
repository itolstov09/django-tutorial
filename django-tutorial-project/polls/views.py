from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Функция index из приложения polls")