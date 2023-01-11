from django import forms
from django.core.exceptions import ValidationError

valid_coupons = [
    '2020LOVE'
]

class CheckoutForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255)
    coupon = forms.CharField(label='Coupon Code', max_length=255, required=False)

    def clean_coupon(self):
        data = self.cleaned_data['coupon']
        print('data: "{}"'.format(data))
        if data == "":
            data = None
        else:
            if data not in valid_coupons:
                raise ValidationError("Invalid coupon code")
        return data

