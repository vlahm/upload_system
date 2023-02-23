from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def viz(request):
    """View function for home page of site."""
    context = {
        'macrosheds': 'is working on making an viz app'
    }
    # Render the HTML template viz.html with the data in the context variable
    return render(request, 'viz.html', context=context)
