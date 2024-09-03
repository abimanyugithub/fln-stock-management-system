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
    
class CreateWarehouse(TemplateView):
    # model = Warehouse
    # form_class = WarehouseForm
    template_name = 'warehouse/create_warehouse.html'
    # success_url = reverse_lazy('warehouse_view')

    '''def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Initialize the form and add it to the context
        context['warehouse_form'] = WarehouseForm()
        context['area_form'] = AreaForm()
        return context'''
    
    def get(self, request, *args, **kwargs):
        # Initialize the forms
        warehouse_form = WarehouseForm()
        area_form = AreaForm()
        # Fetch provinces from the database
        # provinces = Province.objects.all()

        return render(request, self.template_name, {
            'warehouse_form': warehouse_form,
            'area_form': area_form,
            # 'provinces': provinces,  # Add provinces to the context
        })
    
    def post(self, request, *args, **kwargs):
        # Check which form is submitted using a hidden field or form button names
        if 'submit_warehouse_form' in request.POST:
            warehouse_form = WarehouseForm(request.POST)
            if warehouse_form.is_valid():
                warehouse_form.save()
                return redirect('warehouse_view')  # Change 'success_page' to your desired URL name
            else:
                area_form = AreaForm()  # Empty area form if warehouse form is being submitted

        elif 'submit_area_form' in request.POST:
            area_form = AreaForm(request.POST)
            if area_form.is_valid():
                area_form.save()
                return redirect('warehouse_view')  # Change 'success_page' to your desired URL name
            else:
                warehouse_form = WarehouseForm()  # Empty warehouse form if area form is being submitted

        # If neither form is valid, re-render the template with error messages
        return render(request, self.template_name, {
            'warehouse_form': warehouse_form,
            'area_form': area_form,
        })
    
def load_regencies(request):
    province_id = request.GET.get('province')
    regencies = KabupatenKota.objects.filter(provinsi=province_id).order_by('name')

    # Build the HTML for the options
    options_html = ''.join(
        f'<option value="{regency.id}">{regency.name}</option>'
        for regency in regencies
    )
    script="""
        <script>
            // Clear district and village dropdowns
            $('#district-dropdown').html('<option value=""></option>');
            $('#village-dropdown').html('<option value=""></option>');
        </script>
        """

    return HttpResponse(options_html + script)

def load_districts(request):
    regency_id = request.GET.get('regency')
    districts = Kecamatan.objects.filter(kabupaten_kota=regency_id).order_by('name')
    
    # Build the HTML for the options
    options_html = ''.join(
        f'<option value="{district.id}">{district.name}</option>'
        for district in districts
    )
    script="""
        <script>
            // Clear village dropdowns
            $('#village-dropdown').html('<option value=""></option>');
        </script>
        """

    return HttpResponse(options_html + script)

def load_villages(request):
    district_id = request.GET.get('district')
    villages = KelurahanDesa.objects.filter(kecamatan=district_id).order_by('name')
    
    # Build the HTML for the options
    options_html = ''.join(
        f'<option value="{village.id}">{village.name}</option>'
        for village in villages
    )

    return HttpResponse(options_html)

def load_postal(request):
    village_id = request.GET.get('village')
    postal_codes = KelurahanDesa.objects.get(id=village_id)
    postal_code = postal_codes.postal_code
    
    # Assuming field_name is provided in some way; ensure it's safe for HTML
    field_name = "{{ field.html_name }}"  # This needs to be managed properly if it's a Django template

    # Safely format the postal code and field name into HTML
    html = f'<input type="text" class="form-control" name="{field_name}" id="portal-input" value="{postal_code}"/>'
    return HttpResponse(html)

'''def load_cities(request):
    # Extract the 'state_id' parameter from the request
    state_id = request.GET.get('state_id')
    
    # Handle the case where 'state_id' might not be provided
    if not state_id:
        return HttpResponse('<select name="city" id="id_city"><option value="">Select City</option></select>')

    # Query the database for cities based on the state_id
    cities = City.objects.filter(state_id=state_id).all()
    
    # Build HTML for city dropdown
    html = '<select name="city" id="id_city">'
    html += '<option value="">Select City</option>'
    for city in cities:
        html += f'<option value="{city.id}">{city.name}</option>'
    if not cities:
        html += '<option value="">No cities available</option>'
    html += '</select>'
    
    return HttpResponse(html)'''
   

'''def load_cities(request):
    state_id = request.GET.get('state_id')
    cities = City.objects.filter(state_id=state_id).all()
    
    # Build HTML for city dropdown
    html = '<select name="city" id="id_city">'
    html += '<option value="">Select City</option>'
    for city in cities:
        html += f'<option value="{city.id}">{city.name}</option>'
    if not cities:
        html += '<option value="">No cities available</option>'
    html += '</select>'
    
    return HttpResponse(html)'''

'''def load_cities(request):
    state_id = request.GET.get('state_id')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    city_options = '<option value="">Select a city</option>'
    for city in cities:
        city_options += f'<option value="{city.id}">{city.name}</option>'
    return HttpResponse(city_options)'''

class CreateArea(CreateView):
    model = Area
    form_class = AreaForm 
    #template_name = 'warehouse/create_warehouse.html'
    template_name = 'area/form.html'
    success_url = reverse_lazy('warehouse_view')