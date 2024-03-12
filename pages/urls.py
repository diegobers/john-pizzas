from django.urls import path

from .views import IndexTemplateView


urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),
]