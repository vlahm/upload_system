from django.shortcuts import render
from django.http import HttpResponse
from upload.forms import ProductForm

# original "upload" landing page
def upload(request):
    """View function for home page of site."""
    context = {
        'macrosheds': 'is working on making an upload app'
    }
    # Render the HTML template upload.html with the data in the context variable
    return render(request, 'upload.html', context=context)

# first step - does intended upload have minimum required data
def upload_requirements(request):
    """view page where uploading user checks minimum data requirements for MacroSheds upload"""
    context = {
        'macrosheds': 'is working on making an upload app'
    }
    # Render the HTML template upload.html with the data in the context variable
    return render(request, 'upload_requirements.html', context=context)

# second step - what products do you plan to upload?
def upload_plan(request):
    """view page where uploading user indicates data products they plan to upload to MacroSheds"""
    context = {
        'macrosheds': 'is working on making an upload app'
    }
    # Render the HTML template upload.html with the data in the context variable
    return render(request, 'upload_plan.html', context=context)

# second step - what products do you plan to upload?
def upload_product(request):
    """view"""
    context = {}

    # create object of form
    form = ProductForm(request.POST or None)

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()

    context['form'] = form

    # Render the HTML template upload.html with the data in the context variable
    return render(request, 'name.html', {'form': form})
