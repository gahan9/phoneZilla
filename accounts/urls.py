# coding=utf-8
from django.contrib.auth.views import login as django_login, logout as django_logout
from django.conf.urls.static import static
from django.urls import path

from inventory_management.forms import *
from core_settings import settings

urlpatterns = [
    # Login Logout
    path('login/', django_login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    path('logout/', django_logout, {'next_page': '/login/'}, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
