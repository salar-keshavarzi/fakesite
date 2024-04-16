from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, reverse, redirect
from rest_framework.generics import CreateAPIView
from account.models import UserModel, LoginCode
from product.models import Product, ProductImage
from django.views import View
from account.serializers import LoginCodeSerializer
from django.contrib.auth import authenticate, logout, login
import time
from lib.throttle import LoginThrottle1, LoginThrottle2


@login_required
def test(request):
    images = ProductImage.objects.all()
    return render(request, template_name='test.html', context={'images': images})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return render(request, template_name='auth/login.html', context={'step': 1})

    def post(self, request):
        phone_number = request.POST.get('phone-number-hidden', None)
        otp_code = request.POST.get('otp-hidden', None)
        if phone_number and len(phone_number.strip()) == 11 and otp_code:
            username = phone_number.strip()
            otp = otp_code.strip()
            user = authenticate(username=username, password=otp)
            if user:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('home')
            else:
                user = UserModel.objects.filter(username=phone_number).first()
                if user:
                    temp_time = 120 - int(time.time() - user.last_otp)
                    remaining_time = temp_time if temp_time > 0 else 120
                    return render(request, template_name='auth/login.html',
                                  context={'step': 2, 'phone_number': phone_number, 'remaining_time': remaining_time})
        return render(request, template_name='auth/login.html', context={'step': 1})


# def confirm_login(username, password, remaining_time, next):
#     pass


class LoginAPI(CreateAPIView):
    queryset = LoginCode.objects.all()
    serializer_class = LoginCodeSerializer
    throttle_classes = [LoginThrottle1, LoginThrottle2]


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
