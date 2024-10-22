from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard_view'),
    path('warehouse/', views.ListWarehouse.as_view(), name='warehouse_view'),
    path('warehouse/create/', views.WarehouseCreateView.as_view(), name='warehouse_create'),
    path('area/create/', views.CreateArea.as_view(), name='area_create'),
    #path('htmx/load-regencies/', views.load_regencies, name='htmx_load_regencies'),
    #path('htmx/load-districts/', views.load_districts, name='htmx_load_districts'),
    #path('htmx/load-villages/', views.load_villages, name='htmx_load_villages'),
    #path('htmx/load-postal-code/', views.load_postal, name='htmx_load_postal'),
    path('kabupaten-kota/', views.get_kabupaten_kota, name='get_kabupaten_kota'),
    path('kecamatan/', views.get_kecamatan, name='get_kecamatan'),
    path('kelurahan-desa/', views.get_kelurahan_desa, name='get_kelurahan_desa'),
]
