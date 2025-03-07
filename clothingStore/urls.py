"""clothingStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView
from account.views import LoginView, LoginAPI, LogOutView

urlpatterns = [
                  path('salidev/admin/', admin.site.urls),
                  path('user/', include('account.urls')),
                  path('product/', include('product.urls')),
                  path('activity/', include('activity.urls')),
                  path('basket/', include('basket.urls')),
                  path('order/', include('order.urls')),
                  path('manager/', include('manager.urls')),
                  path('login/', LoginView.as_view(), name='login'),
                  path('login/api/', LoginAPI.as_view(), name='login-api'),
                  path('logout/', LogOutView.as_view(), name='logout'),
                  path('', TemplateView.as_view(template_name='index.html'), name='home'),
                  path('about/', TemplateView.as_view(template_name='about-us.html'), name='about-us'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
