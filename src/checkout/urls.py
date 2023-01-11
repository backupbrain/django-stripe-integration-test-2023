from django.urls import path
from .views import (
	CheckoutView,
	CheckoutSuccessView,
	CheckoutErrorView,
)

urlpatterns = [
    path('', CheckoutView.as_view(), name='checkout'),
    path('success/', CheckoutSuccessView.as_view(), name="checkout_success"),
    path('error/', CheckoutErrorView.as_view(), name="checkout_error"),
]
