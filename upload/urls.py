#!/usr/bin/env python3
from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload, name='upload'),
    path('requirements', views.upload_requirements, name='upload_requirements'),
    path('plan', views.upload_plan, name='upload_plan')
    # path('product', views.upload_product, name='upload_product'),
]
