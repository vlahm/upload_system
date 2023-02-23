from django.shortcuts import render
from django.http import HttpResponse

# original "user" landing page
def user(request):
    """View function for home page of site."""
    context = {
        'macrosheds': 'is working on making an user app'
    }
    # Render the HTML template user.html with the data in the context variable
    return render(request, 'user.html', context=context)
