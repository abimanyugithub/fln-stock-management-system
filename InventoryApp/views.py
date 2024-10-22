from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView
from .models import Warehouse, Area
# from .forms import Country, State, WarehouseForm, AreaForm  # Import your form if needed
# from .forms import Province, Regency, District, Village, WarehouseForm, AreaForm
from .forms import Provinsi, KabupatenKota, Kecamatan, KelurahanDesa, WarehouseForm, AreaForm


# Create your views here.
class Dashboard(TemplateView):
    template_name = 'index.html'

class ListWarehouse(ListView):
    model = Warehouse
    template_name = 'warehouse/list_warehouse.html'
    context_object_name = 'wh'

    def get_context_data(self, **kwargs):
        # Memanggil implementasi dasar untuk mendapatkan context yang ada
        context = super().get_context_data(**kwargs)
        # Menambahkan header tabel dinamis ke dalam context
        context['table_headers'] = ['Name', 'Capacity', 'Manager', 'Inventory Count', 'Created at', 'Updated at']
        return context
    
def get_kabupaten_kota(request):
    provinsi_id = request.GET.get('province')
    kabupaten_kota = KabupatenKota.objects.filter(provinsi=provinsi_id).order_by('name')
    options = '<option value="">Pilih Kabupaten/Kota</option>'
    for item in kabupaten_kota:
        options += f'<option value="{item.id}">{item.name}</option>'
    return HttpResponse(options)

def get_kecamatan(request):
    kabupaten_kota_id = request.GET.get('regency')
    kecamatan = Kecamatan.objects.filter(kabupaten_kota_id=kabupaten_kota_id)
    options = '<option value="">Pilih Kecamatan</option>'
    for item in kecamatan:
        options += f'<option value="{item.id}">{item.name}</option>'
    return HttpResponse(options)

def get_kelurahan_desa(request):
    kecamatan_id = request.GET.get('district')
    kelurahan_desa = KelurahanDesa.objects.filter(kecamatan_id=kecamatan_id)
    options = '<option value="">Pilih Kelurahan/Desa</option>'
    for item in kelurahan_desa:
        options += f'<option value="{item.id}">{item.name} - {item.postal_code}</option>'
    return HttpResponse(options)

class WarehouseCreateView(CreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name = 'warehouse/create_warehouse.html'
    success_url = reverse_lazy('warehouse_list')  # Ganti dengan URL setelah sukses

    def form_valid(self, form):
        # Tambahkan logika tambahan jika perlu
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Initialize the form and add it to the context
        context['disable_form'] = ['province', 'regency', 'district', 'village']
        return context
    
class CreateArea(CreateView):
    model = Area
    form_class = AreaForm 
    #template_name = 'warehouse/create_warehouse.html'
    template_name = 'area/form.html'
    success_url = reverse_lazy('warehouse_view')