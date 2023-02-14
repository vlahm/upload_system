from django.shortcuts import render
from django.http import HttpResponse


def download(request):
    return HttpResponse("Hello, world. You're at MacroSheds: download.")
