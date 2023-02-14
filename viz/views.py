from django.shortcuts import render
from django.http import HttpResponse


def viz(request):
    return HttpResponse("Hello, world. You're at MacroSheds: viz.")
