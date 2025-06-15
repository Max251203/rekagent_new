from django.urls import path
from . import views_clients

urlpatterns = [
    path('', views_clients.client_list, name='client_list'),
]
