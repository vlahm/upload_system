from django.shortcuts import render

# Create your views here.
def index(request):
    """View function for home page of site."""
    context = {
        'macrosheds': 'is the coolest'
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# Create your views here.
def upload(request):
    """View function for home page of site."""
    context = {
        'macrosheds': 'is working on making an upload app'
    }
    # Render the HTML template upload.html with the data in the context variable
    return render(request, 'upload.html', context=context)
