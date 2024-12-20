from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from .models import Warehouse, Area, Category, Product, UOM, ProductType
# from .forms import Country, State, WarehouseForm, AreaForm  # Import your form if needed
# from .forms import Province, Regency, District, Village, WarehouseForm, AreaForm
from .forms import Provinsi, KabupatenKota, Kecamatan, KelurahanDesa, WarehouseForm, AreaForm, CategoryForm, ProductForm, UOMForm, ProductTypeForm
from django.contrib import messages

# Create your views here.
class Dashboard(TemplateView):
    template_name = 'InventoryApp/index.html'


class WarehouseListView(ListView):
    model = Warehouse
    template_name = 'InventoryApp/warehouse/list.html'
    context_object_name = 'list_item'
    ordering = ['code']

    def get_context_data(self, **kwargs):
        # Memanggil implementasi dasar untuk mendapatkan context yang ada
        context = super().get_context_data(**kwargs)
        # Menambahkan header tabel dinamis ke dalam context
        context['fields'] = {
            'code': 'Warehouse Code',
            'name': 'Warehouse Name',
            'zone': 'Zone',
            'phone_number': 'Phone Number',
            'email': 'Email Address',
            'manager': 'Manager'
        }

        context['breadcrumb'] = [
            {'name': 'Home', 'url': 'dashboard_view'},
            {'name': 'Warehouse', 'url': 'warehouse_list'},
            {'name': 'List', 'url': None}  # No URL for the last breadcrumb item
        ]

        return context
    
    
def get_kabupaten_kota(request):
    provinsi_id = request.GET.get('province')
    kabupaten_kota = KabupatenKota.objects.filter(provinsi=provinsi_id).order_by('name')
    options = '<option value="">Select Regency/City</option>'
    for item in kabupaten_kota:
        options += f'<option value="{item.id}">{item.name}</option>'
    return HttpResponse(options)

def get_kecamatan(request):
    kabupaten_kota_id = request.GET.get('regency')
    kecamatan = Kecamatan.objects.filter(kabupaten_kota_id=kabupaten_kota_id)
    options = '<option value="">Select District</option>'
    for item in kecamatan:
        options += f'<option value="{item.id}">{item.name}</option>'
    return HttpResponse(options)

def get_kelurahan_desa(request):
    kecamatan_id = request.GET.get('district')
    kelurahan_desa = KelurahanDesa.objects.filter(kecamatan_id=kecamatan_id)
    options = '<option value="">Select Village/Subdistrict</option>'
    for item in kelurahan_desa:
        options += f'<option value="{item.id}">{item.name}, {item.postal_code}</option>'
    return HttpResponse(options)


class WarehouseCreateView(CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'InventoryApp/warehouse/create.html'
    success_url = reverse_lazy('warehouse_list')  # Ganti dengan URL setelah sukses

    def form_valid(self, form):
        # Call the parent class's form_valid method to save the warehouse
        response = super().form_valid(form)  
        
        # Get the name of the newly created warehouse
        warehouse_code = form.cleaned_data['code']  # Assuming 'code' is the field name in your form
        warehouse_name = form.cleaned_data['name']  # Assuming 'name' is the field name in your form
        
        # Add a success message including the warehouse name and code
        messages.success(self.request, f'Warehouse "{warehouse_name}" (Code: {warehouse_code}) created successfully!')

        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Initialize the form and add it to the context
        context['disable_fields'] = ['province', 'regency', 'district', 'village']
        return context
    
    
class WarehouseUpdateView(UpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'InventoryApp/warehouse/update.html'
    success_url = reverse_lazy('warehouse_list')  # Ganti dengan URL setelah sukses
    context_object_name = 'warehouse'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # Filter queryset untuk field kabupaten berdasarkan provinsi
        if form.instance.province:
            form.fields['regency'].queryset = KabupatenKota.objects.filter(provinsi=form.instance.province)

        # Filter queryset untuk field district berdasarkan kabupaten
        if form.instance.regency:
            form.fields['district'].queryset = Kecamatan.objects.filter(kabupaten_kota=form.instance.regency)

        # Filter queryset untuk field village berdasarkan district
        if form.instance.district:
            form.fields['village'].queryset = KelurahanDesa.objects.filter(kecamatan=form.instance.district)

        return form

    def form_valid(self, form):
        # Call the parent class's form_valid method to update the warehouse
        response = super().form_valid(form)

        # Get the updated name and code of the warehouse
        warehouse_code = form.cleaned_data['code']  # Assuming 'code' is the field name in your form
        warehouse_name = form.cleaned_data['name']  # Assuming 'name' is the field name in your form
        
        # Add a success message including the updated warehouse name and code
        messages.success(self.request, f'Warehouse "{warehouse_name}" (Code: {warehouse_code}) updated successfully!')

        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Initialize the form and add it to the context
        context['disable_fields'] = ['province', 'regency', 'district', 'village']
        return context
    
    
class AreaListView(ListView):
    model = Area
    template_name = 'area/list.html'
    context_object_name = 'list_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for item in context['list_item']:
            item.get_zone = item.warehouse.zone

        context['fields'] = {
            'warehouse': 'Warehouse',
            'get_zone': 'Zone Name',
            'area_name': 'Area Name',
            'capacity': 'Capacity'
            }
        return context


class AreaCreateView(CreateView):
    model = Area
    form_class = AreaForm 
    template_name = 'area/create_or_update.html'
    success_url = reverse_lazy('area_list')


class AreaUpdateView(UpdateView):
    model = Area
    form_class = AreaForm 
    template_name = 'area/create_or_update.html'
    success_url = reverse_lazy('area_list')

class UOMCreateView(CreateView):
    model = UOM
    form_class = UOMForm 
    template_name = 'InventoryApp/uom/create_or_update.html'
    success_url = reverse_lazy('uom_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class UOMUpdateView(UpdateView):
    model = UOM
    form_class = UOMForm 
    template_name = 'InventoryApp/uom/create_or_update.html'
    success_url = reverse_lazy('uom_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        return context


class UOMListView(ListView):
    model = UOM
    template_name = 'InventoryApp/uom/list.html'
    context_object_name = 'list_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['fields'] = {
            'name': 'Name',
            'code': 'Code',
            'description': 'Description',
            }
        return context
    

class ProductTypeCreateView(CreateView):
    model = ProductType
    form_class = ProductTypeForm 
    template_name = 'product_type/create_or_update.html'
    success_url = reverse_lazy('type_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class ProductTypeUpdateView(UpdateView):
    model = ProductType
    form_class = ProductTypeForm 
    template_name = 'product_type/create_or_update.html'
    success_url = reverse_lazy('type_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        return context


class ProductTypeListView(ListView):
    model = ProductType
    template_name = 'product_type/list.html'
    context_object_name = 'list_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['fields'] = {
            'name': 'Name',
            'code': 'Code',
            'description': 'Description',
            'created_at': 'Registered Date',
            'updated_at': 'Updated Date'
            }
        return context


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm 
    template_name = 'category/create_or_update.html'
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm 
    template_name = 'category/create_or_update.html'
    success_url = reverse_lazy('category_list')


class CategoryListView(ListView):
    model = Category
    template_name = 'category/list.html'
    context_object_name = 'list_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['fields'] = {
            'name': 'Category Name',
            'description': 'Description',
            'created_at': 'Registered Date',
            'updated_at': 'Updated Date'
            }
        return context


class ProductCreatetView(CreateView):
    model = Product
    form_class = ProductForm 
    template_name = 'product/create_or_update.html'
    success_url = reverse_lazy('product_list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm 
    template_name = 'product/create_or_update.html'
    success_url = reverse_lazy('product_list')


class ProductListView(ListView):
    model = Product
    template_name = 'product/list.html'
    context_object_name = 'list_item'

    def get_context_data(self, **kwargs):
        # Memanggil implementasi dasar untuk mendapatkan context yang ada
        context = super().get_context_data(**kwargs)
        
        # Menambahkan header tabel dinamis ke dalam context
        context['fields'] = {
            'sku': 'Code',
            'name': 'Name',
            'category': 'Category',
            'uom': 'Unit',
            'product_type': 'Type',
            # 'description': 'Description',
            'created_at': 'Registered Date',
            'updated_at': 'Updated Date'
            }
        return context