from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard_view'),
    path('warehouse/', views.ListWarehouse.as_view(), name='warehouse_view'),
    path('warehouse/create/', views.CreateWarehouse.as_view(), name='warehouse_create'),
    path('area/create/', views.CreateArea.as_view(), name='area_create'),
    '''path('htmx/load-states/', views.load_states, name='htmx_load_states'),
    path('htmx/load-cities/', views.load_cities, name='htmx_load_cities'),'''
]
