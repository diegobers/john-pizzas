from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView
from . import views
from allauth.account.views import SignupView, LoginView as LoginAllAtht


urlpatterns = [
    path('', LoginView.as_view(template_name ='accounts/login.html'), name='login'),
    path('cadastro/', SignupView.as_view(template_name ='accounts/signup.html'), name='signup'),
    path('entrar/', LoginAllAtht.as_view(template_name ='accounts/signin.html'), name='signin'),
    path('sair/', LogoutView.as_view(next_page='index'), name='logout'),
    path('painel/', views.dashboard, name='dashboard'),
]