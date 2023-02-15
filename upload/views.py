from django.shortcuts import render
from django.http import HttpResponse


# def upload(request):
#     return HttpResponse("Hello, world. You're at MacroSheds: upload.")

# Create your views here.
def upload(request):
    """View function for home page of site."""
    context = {
        'macrosheds': 'is working on making an upload app'
    }
    # Render the HTML template upload.html with the data in the context variable
    return render(request, 'upload.html', context=context)
