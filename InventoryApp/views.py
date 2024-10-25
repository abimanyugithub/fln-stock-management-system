from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from .models import Warehouse, Area
# from .forms import Country, State, WarehouseForm, AreaForm  # Import your form if needed
# from .forms import Province, Regency, District, Village, WarehouseForm, AreaForm
from .forms import Provinsi, KabupatenKota, Kecamatan, KelurahanDesa, WarehouseForm, AreaForm
from django.contrib import messages


# Create your views here.
class Dashboard(TemplateView):
    template_name = 'index.html'


class WarehouseListView(ListView):
    model = Warehouse
    template_name = 'warehouse/list_warehouse.html'
    context_object_name = 'list_warehouse'
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
            'manager': 'Manager'}
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
    template_name = 'warehouse/create_warehouse.html'
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
    template_name = 'warehouse/update_warehouse.html'
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
    template_name = 'area/list_area.html'
    context_object_name = 'list_area'

    def get_context_data(self, **kwargs):
        # Memanggil implementasi dasar untuk mendapatkan context yang ada
        context = super().get_context_data(**kwargs)
        # Menambahkan header tabel dinamis ke dalam context
        context['fields'] = {
            'code': 'Warehouse Code',
            'name': 'Warehouse Name',
            'location': 'Location',
            'phone_number': 'Phone Number',
            'email': 'Email Address',
            'manager': 'Manager'}
        return context


class AreaCreateView(CreateView):
    model = Area
    form_class = AreaForm 
    template_name = 'area/create_area.html'
    # template_name = 'area/form.html'
    success_url = reverse_lazy('warehouse_view')