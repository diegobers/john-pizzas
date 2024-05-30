from django import forms
from .models import Order, Pizza


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'price']


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['is_shipping', 'shipping_address', 'payment_method', 'observation']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['is_shipping'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['shipping_address'].widget.attrs.update({'class': 'form-control'})
        self.fields['payment_method'].widget.attrs.update({'class': 'form-control'})
        self.fields['observation'].widget.attrs.update({'class': 'form-control'})
        
        if user:
            self.fields['shipping_address'].initial = user.address if user else ''