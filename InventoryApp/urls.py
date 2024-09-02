from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard_view'),
    path('warehouse/', views.ListWarehouse.as_view(), name='warehouse_view'),
    path('warehouse/create/', views.CreateWarehouse.as_view(), name='warehouse_create'),
    path('area/create/', views.CreateArea.as_view(), name='area_create'),
    path('htmx/load-regencies/', views.load_regencies, name='htmx_load_regencies'),
    path('htmx/load-districts/', views.load_districts, name='htmx_load_districts'),
]
