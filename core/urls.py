from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    #path('pizzas-show/', include("pages.urls")),
    path('entrar/', include("accounts.urls")),
    #path('pedidos/', include("orders.urls")),
    #path('carrinho/', include("cart.urls")),
    path('contas/', include('allauth.urls')),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)