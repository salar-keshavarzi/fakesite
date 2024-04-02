from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model


# @login_required
def test(request):
    print(request.user.get_basket())
    return HttpResponse('test')
