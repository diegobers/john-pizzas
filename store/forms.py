from django import forms
from .models import Order, Pizza

from django.utils.translation import gettext_lazy as _
from django_bootstrap5.widgets import RadioSelectButtonGroup



class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'price']



class CartCheckoutForm(forms.ModelForm):
    SHIPPING_CHOICES = [
        (True, _('Entregar')),
        (False, _('Retirar'))
    ]

    is_shipping = forms.ChoiceField(
        choices=SHIPPING_CHOICES, 
        widget=RadioSelectButtonGroup(),
        initial=True,
    )

    class Meta:
        model = Order
        fields = ['is_shipping', 'shipping_address', 'payment_method', 'observation']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Update widget attributes for form fields
        self.fields['is_shipping'].widget.attrs.update({'class': 'form-check-input btn-check', 'autocomplete': 'off'})
        self.fields['shipping_address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Rua...'})
        self.fields['payment_method'].widget.attrs.update({'class': 'form-control'})
        self.fields['observation'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Observação...'})
        
        # Customize label classes
        self.fields['shipping_address'].label = _('Endereço')
        self.fields['payment_method'].label = _('Forma de Pagamento')
        self.fields['observation'].label = _('Obrservação...')
        
        if user:
            self.fields['shipping_address'].initial = user.address if user else ''

