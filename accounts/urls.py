# coding=utf-8
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.urls import path

from inventory_management.forms import LoginForm
from core_settings import settings

urlpatterns = [
    # Login Logout
    path('login/', LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
