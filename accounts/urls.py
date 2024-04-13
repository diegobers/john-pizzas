from django.urls import path, include

from allauth.account.views import SignupView, LoginView, LogoutView


app_name = 'accounts'

urlpatterns = [
    path('cadastro/', SignupView.as_view(template_name ='accounts/signup.html'), name='signup'),
    path('', LoginView.as_view(template_name ='accounts/signin.html'), name='signin'),
    path('sair/', LogoutView.as_view(), name='logout'),
]