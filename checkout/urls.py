from django.urls import path
from .views import checkout, checkout_success, checkout_cancel

urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('success/', checkout_success, name='checkout_success'),
    path('cancel/', checkout_cancel, name='checkout_cancel'),
]
