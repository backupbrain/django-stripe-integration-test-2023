from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from django.views.generic.base import TemplateView
from django.conf import settings
from .forms import CheckoutForm
import stripe
import json


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = '2022-11-15'

charge_amount = 649
stripe_product_id = 'prod_N8GtP4kfDmf5Wn'
stripe_sku = 'sku_GOdUWWauNOfRgU'

class CheckoutView(View):

    template_file = 'checkout/checkout.html'
    form_class = CheckoutForm

    def get_context_data(self, **kwargs):
        context = {}
        context['requent'] = self.request
        form = self.form_class(self.request.POST)
        context['form'] = form
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            intent = stripe.PaymentIntent.create(
              amount=charge_amount,
              currency='usd',
              # Verify your integration in this guide by including this parameter
              metadata={'integration_check': 'accept_a_payment'},
            )
            context['client_secret'] = intent.client_secret
        except stripe.error.StripeError as e:
            return HttpResponse('Error creating stripe payment intent: {}.'.format(str(e)))
        except Exception as e:
            return HttpResponse('Error creating stripe payment intent: {}.'.format(str(e)))
        return render(request, self.template_file, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = context['form']
        print(form.errors)
        if form.is_valid():
            email = form.cleaned_data['email']
            coupon = form.cleaned_data['coupon']
            print('email: {}'.format(email))
            print('coupon: {}'.format(coupon))
            coupons = stripe.Coupon.list()
            print(coupons)
            try:
                session = stripe.checkout.Session.create(
                    customer_email=email,
                    line_items=[{
                        'price': stripe_sku,
                        'quantity': 1,
                    }],
                    discounts=[{
                        'coupon': coupon
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri('/success')
                )
                return redirect('checkout_success')
            except Exception as e:
                print(e)
                return redirect('checkout_error')
        return render(request, self.template_file, context)


class CheckoutSuccessView(TemplateView):

    template_name = 'checkout/checkout_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        return context


class CheckoutErrorView(TemplateView):

    template_name = 'checkout/checkout_error.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        return context
