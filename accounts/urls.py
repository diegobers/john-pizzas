from django.urls import path, include

from allauth.account.views import LogoutView
from accounts.views import CustomLoginView, CustomSignupView


app_name = 'accounts'

urlpatterns = [
    path('cadastro/', CustomSignupView.as_view(), name='signup'),
    path('', CustomLoginView.as_view(), name='login'),
    path('sair/', LogoutView.as_view(), name='logout'),
]