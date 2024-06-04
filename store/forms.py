from django import forms
from .models import Order, Pizza

from django.utils.translation import gettext_lazy as _



class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'price']


class CartCheckoutForm(forms.ModelForm):
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
        

        # Add custom Bootstrap 5 classes to labels
        self.fields['is_shipping'].label = _('Entregar?')
        self.fields['shipping_address'].label = _('Endereço')
        self.fields['payment_method'].label = _('Forma de Pagamento:')

        if user:
            self.fields['shipping_address'].initial = user.address if user else ''