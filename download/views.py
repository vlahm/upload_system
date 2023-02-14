from django.shortcuts import render
from django.http import HttpResponse


# def download(request):
#     return HttpResponse("Hello, world. You're at MacroSheds: download.")

# Create your views here.
def download(request):
    """View function for home page of site."""
    context = {
        'macrosheds': 'is working on making an download app'
    }
    # Render the HTML template download.html with the data in the context variable
    return render(request, 'download.html', context=context)
