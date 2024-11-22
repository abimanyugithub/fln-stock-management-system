from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard_view'),

    # warehouse
    path('warehouse/', views.WarehouseListView.as_view(), name='warehouse_list'),
    path('warehouse/create/', views.WarehouseCreateView.as_view(), name='warehouse_create'),
    path('warehouse/update/<uuid:pk>/', views.WarehouseUpdateView.as_view(), name='warehouse_update'),
    # area
    path('area/', views.AreaListView.as_view(), name='area_list'),
    path('area/create/', views.AreaCreateView.as_view(), name='area_create'),
    path('area/update/<uuid:pk>/', views.AreaUpdateView.as_view(), name='area_update'),

    # uom
    path('uom/', views.UOMListView.as_view(), name='uom_list'),
    path('uom/create/', views.UOMCreateView.as_view(), name='uom_create'),
    path('uom/update/<uuid:pk>/', views.UOMUpdateView.as_view(), name='uom_update'),

    # type
    path('type/', views.ProductTypeListView.as_view(), name='type_list'),
    path('type/create/', views.ProductTypeCreateView.as_view(), name='type_create'),
    path('type/update/<uuid:pk>/', views.ProductTypeUpdateView.as_view(), name='type_update'),

    # product category
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<uuid:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    # product
    path('product/', views.ProductListView.as_view(), name='product_list'),
    path('product/create/', views.ProductCreatetView.as_view(), name='product_create'),
    path('product/update/<uuid:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
    #path('htmx/load-regencies/', views.load_regencies, name='htmx_load_regencies'),
    #path('htmx/load-districts/', views.load_districts, name='htmx_load_districts'),
    #path('htmx/load-villages/', views.load_villages, name='htmx_load_villages'),
    #path('htmx/load-postal-code/', views.load_postal, name='htmx_load_postal'),
    path('kabupaten-kota/', views.get_kabupaten_kota, name='get_kabupaten_kota'),
    path('kecamatan/', views.get_kecamatan, name='get_kecamatan'),
    path('kelurahan-desa/', views.get_kelurahan_desa, name='get_kelurahan_desa'),
]
