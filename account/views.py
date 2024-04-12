from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model

from product.models import Product, ProductImage


# @login_required
def test(request):
    images = ProductImage.objects.all()
    return render(request, template_name='test.html', context={'images': images})
