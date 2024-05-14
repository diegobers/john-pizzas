from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    #path('pizzas-show/', include("pages.urls")),
    path('contas/', include("accounts.urls")),
    #path('pedidos/', include("orders.urls")),
    #path('carrinho/', include("cart.urls")),
    path('contas/', include('allauth.urls')),
    path('contas/', include('allauth.socialaccount.urls')),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)