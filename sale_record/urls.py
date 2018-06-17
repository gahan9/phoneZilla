from django.urls import path

from .views import *

urlpatterns = [
    path('generate_invoice/<int:pk>/', InvoiceGenerateView.as_view(), name="generate_invoice"),
]
