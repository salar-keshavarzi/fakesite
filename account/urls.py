from django.urls import path
from account.views import test

urlpatterns = [
    path('test/', test, name="test")
]
