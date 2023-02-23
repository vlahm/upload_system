from django.shortcuts import render

# Create your views here.
def landing(request):
    """View function for home page of site."""
    context = {
        'macrosheds': 'is the coolest'
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'landing.html', context=context)
