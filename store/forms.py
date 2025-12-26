from django import forms
from .models import Product
from .models import CartItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'stock', 'banner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}), # Add 'stock' field with NumberInput widget to show stock quantity in the form.
        }



class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']  # Specify the fields you want in the form
        widgets = {
            'product': forms.HiddenInput(),  # Hide the product field in the form
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),  # Display quantity as a number input
        }
