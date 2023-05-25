from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from upload.forms import ProductForm
from upload.models import Product
from .forms import UploadFileForm
from upload_system.helpers import handle_uploaded_file

# original "upload" landing page
def upload(request):
    """View function for home page of site."""
    context = {}
    context['user_active'] = request.user.is_authenticated

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

# # second step - what products do you plan to upload?
# def upload_plan(request):
#     """view page where uploading user indicates data products they plan to upload to MacroSheds"""
#     context = {
#         'macrosheds': 'is working on making an upload app'
#     }
#     # Render the HTML template upload.html with the data in the context variable
#     return render(request, 'upload_plan.html', context=context)

# second step - what products do you plan to upload?
def upload_plan(request):
    """view"""
    context = {}
    products = Product.objects.all()

    # create object of form
    form = ProductForm(request.POST)

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        prod_instance = form.save(commit = False)
        prod_instance.user = request.user
        prod_instance.save()

    context['form'] = form
    context['products'] = products

    # Render the HTML template upload.html with the data in the context variable
    return render(request, 'upload_plan.html', {'form': form, 'products': products})

def upload_sitedata(request):
    context = {}
    return render(request, 'upload_sitedata.html', context=context)

def upload_timeseries(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fn = form.files['file'].name
            matches = handle_uploaded_file(request.FILES['file'], 'data/uploads_ts/' + fn)
            return render(request, 'upload_matchcolumns.html', context = {'matches': matches})
    else:
        form = UploadFileForm()
    return render(request, 'upload_timeseries.html', context={'form': form})

def upload_matchcolumns(request):
    context = {}
    return render(request, 'upload_matchcolumns.html', context=context)

def upload_units(request):
    context = {}
    selections = dict(request.POST.copy().lists())
    del selections['csrfmiddlewaretoken']
    del selections['post_categories']

    if request.method == 'POST':
        print(request.POST)
        context['input_cols'] = selections
    else:
        print('user column matches POST failed, please retry')

    return render(request, 'upload_units.html', context=context)
