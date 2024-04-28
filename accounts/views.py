from allauth.account.views import LoginView, SignupView
from django.urls import reverse_lazy
from store.models import Cart
from django.views.generic import TemplateView


class CustomSignupView(SignupView):
    template_name = 'signup.html'
    success_url = reverse_lazy('store:view_cart') 


class CustomLoginView(LoginView):
    template_name = 'signin.html'
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
        
        return response