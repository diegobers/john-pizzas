from django.urls import path, re_path

from allauth.account.views import LogoutView
from accounts.views import (
    UserProfileView,
    CustomLoginView, 
    CustomSignupView, 
    ResetPasswordView,
    ResetPasswordDoneView,
    ResetPasswordKeyView,
    ResetPasswordKeyDoneView,
)

app_name = 'accounts'

urlpatterns = [
    path('cadastro/', CustomSignupView.as_view(), name='signup'),
    path('', CustomLoginView.as_view(), name='login'),
    #path('login_or_signup/', login_or_signup, name='login_or_signup'),
    path('sair/', LogoutView.as_view(), name='logout'),

    path('edit_profile/', UserProfileView.as_view(), name='edit_profile'),



    # password reset
    path('recuperar-senha/', ResetPasswordView.as_view(), name="reset_password"),
    path('recuperar-senha/link-enviado/', ResetPasswordDoneView.as_view(), name="reset_password_done"),
    

    #path('recuperar-senha/chave/<uidb36>/<key>/',
    #     ResetPasswordKeyView.as_view(),
    #     name='reset_password_key',
    #),

    re_path(
        r"^recuperar-senha/chave/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/",
        ResetPasswordKeyView.as_view(),
        name="reset_password_key",
    ),
    
    path(
        "recuperar-senha/sucesso/",
        ResetPasswordKeyDoneView.as_view(),
        name="reset_password_key_done",
    ),

]