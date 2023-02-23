from django.shortcuts import render
from django.http import HttpResponse


def user(request):
    return HttpResponse("Hello, world. You're at MacroSheds: user.")
