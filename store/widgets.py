from django.forms import RadioSelect


class MyRadioSelectButtonGroup(RadioSelect):
    template_name = "django_bootstrap5/widgets/radio_select_button_group.html"