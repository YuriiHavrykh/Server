from django.urls import path
from . import views

urlpatterns = [
    path('employee/', views.employee_list, name='employee_list'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employee/create/', views.employee_create, name='employee_create'),
    path('employee/<int:pk>/edit/', views.employee_update, name='employee_update'),
    path('employee/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('teams/', views.teams_list, name='teams_list'),
    path('drivers/', views.drivers_list, name='drivers_list')
]
