from django import forms
from allauth.account.forms import LoginForm
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe


class CustomAllAuthLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add custom placeholder texts if needed
        self.fields['login'].widget.attrs['placeholder'] = _('Usuário ou E-mail')
        self.fields['password'].widget.attrs['placeholder'] = _('*********')

        # Add custom Bootstrap 5 classes to labels
        self.fields['login'].label = _('Entrar')
        self.fields['password'].label = _('Senhaa')

        self.fields['password'].help_text = mark_safe('<a href=recuperar-senha/>Recuperar Senha?</a>')