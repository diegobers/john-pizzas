from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('entrar/', include("accounts.urls")),
    path('pizzas/', include("orders.urls")),
    path('contas/', include('allauth.urls')),
]