from django.urls import path
from . import views_positions

urlpatterns = [
    path('', views_positions.position_list, name='position_list'),
    path('create/', views_positions.position_create, name='position_create'),
    path('edit/<int:pk>/', views_positions.position_update, name='position_update'),
    path('delete/<int:pk>/', views_positions.position_delete, name='position_delete'),
]
