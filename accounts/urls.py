from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', LoginView.as_view(template_name ='accounts/login.html'), name='login'),
    path('sair/', LogoutView.as_view(next_page='index'), name='logout'),
]