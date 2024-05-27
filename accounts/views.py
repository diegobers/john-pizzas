from allauth.account.views import LoginView, SignupView
from django.urls import reverse_lazy
from store.models import Cart, Order
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
#from django.views.generic.base import TemplateView, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from allauth.account.forms import LoginForm, SignupForm

from allauth.account.views import PasswordResetView, PasswordResetFromKeyView

from allauth.account.forms import (
    ResetPasswordForm,
    ResetPasswordKeyForm,
)

from .forms import UserProfileForm, UpdateProfileForm


from django.contrib.auth import get_user_model

User = get_user_model()

from .models import JohnPizzaAbstractUserModel

from django.views.generic import (
    UpdateView,
    CreateView, 
    ListView, 
    TemplateView, 
    View, 
    DetailView,
    FormView,
)

class AddressProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'account/add_address.html'
    context_object_name = 'user'
    form_class = UserProfileForm
    success_url = reverse_lazy('accounts:view_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_initial(self):
        # Prefill the form with the current user's data
        initial = super().get_initial()
        initial.update({
            'address': self.request.user.address,
        })
        return initial

        
class EditProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'account/edit_profile.html'
    context_object_name = 'user'
    form_class = UpdateProfileForm
    success_url = reverse_lazy('accounts:view_profile')

    def get_object(self, queryset=None):
        return self.request.user

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'store/dashboard.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(user=self.request.user)
        context['orders'] = orders
        return context


class ResetPasswordView(PasswordResetView):
    template_name = 'account/reset_password.html'
    success_url = reverse_lazy('accounts:reset_password_done')


class ResetPasswordDoneView(TemplateView):
    template_name = 'account/reset_password_done.html'


class ResetPasswordKeyView(PasswordResetFromKeyView):
    template_name = 'account/reset_password_key.html'
    success_url = reverse_lazy('accounts:reset_password_key_done')


class ResetPasswordKeyDoneView(TemplateView):
    template_name = 'account/reset_password_key_done.html'


def login_or_signup(request):
    if request.method == 'POST':
        # If the form is submitted
        if 'login' in request.POST:
            # If the login form is submitted
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                # Redirect to a success page or home page
                return redirect('store:index')
            else:
                signup_form = SignupForm()  # We'll need it if login fails
        else:
            # If the signup form is submitted
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save(request)
                auth_login(request, user)
                # Redirect to a success page or home page
                return redirect('store:index')
            else:
                login_form = LoginForm()  # We'll need it if signup fails
    else:
        # If it's a GET request
        login_form = LoginForm()
        signup_form = SignupForm()
    
    return render(request, 'login_or_signup.html', {'login_form': login_form, 'signup_form': signup_form})


class CustomSignupView(SignupView):
    template_name = 'account/signup.html'
    success_url = reverse_lazy('store:view_cart') 


class CustomLoginView(LoginView):
    template_name = 'account/signin.html'
    success_url = reverse_lazy('store:view_cart') 
    
    def get(self, request, *args, **kwargs):
        request.session['last_session_key'] = request.session.session_key

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        
        last_session_key = self.request.session.get('last_session_key')
        cart_queryset = Cart.objects.filter(session_key=last_session_key)
        
        if cart_queryset.exists():
            cart = cart_queryset.first()
            cart.user_id = self.request.user.id
            cart.session_key = None
            cart.save()
            del self.request.session['last_session_key']
            #messages.success(request, ("Update Cart Items..."))

        return response