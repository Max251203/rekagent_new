from django.urls import path
from . import views_departments

urlpatterns = [
    path('', views_departments.department_list, name='department_list'),
    path('create/', views_departments.department_create, name='department_create'),
    path('edit/<int:pk>/', views_departments.department_update,
         name='department_update'),
    path('delete/<int:pk>/', views_departments.department_delete,
         name='department_delete'),
]
