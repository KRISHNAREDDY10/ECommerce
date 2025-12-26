from django import forms
from checkout.models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'billing_address']  # Add fields you need to capture

    shipping_address = forms.CharField(widget=forms.Textarea, required=True)
    billing_address = forms.CharField(widget=forms.Textarea, required=True)
