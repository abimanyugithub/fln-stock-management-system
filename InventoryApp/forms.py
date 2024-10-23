from django import forms
# from .models import Warehouse, Area, Country, State, City
# from .models import Province, Regency, District, Village, Warehouse, Area
from .models import Provinsi, KabupatenKota, Kecamatan, KelurahanDesa, Warehouse, Area

'''
class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = [
            'code', 'name', 'location', 'capacity', 'manager', 
            'current_inventory', 'address_line1', 'address_line2', 
            'province', 'regency', 'district', 'village', 
            'email', 'phone_number'
        ]
        widgets = {
            'code': forms.TextInput(attrs={'required': True}),
            'name': forms.TextInput(attrs={'required': True}),
            'location': forms.TextInput(attrs={'required': True}),
            'capacity': forms.NumberInput(attrs={'required': True}),
            'current_inventory': forms.NumberInput(attrs={'required': True, 'value': 0}),
            'address_line1': forms.TextInput(attrs={'placeholder': 'Alamat Baris 1'}),
            'address_line2': forms.TextInput(attrs={'placeholder': 'Alamat Baris 2'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Alamat Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Nomor Telepon'}),
        }
'''

class WarehouseForm(forms.ModelForm):

    province = forms.ModelChoiceField(
        queryset=Provinsi.objects.all().order_by('name'),
        label='Province *',
        help_text='Select the province or state (optional).'
    )

    class Meta:
        model = Warehouse
        fields = [
            'code',
            'name',
            'location',
            'capacity',
            'manager',
            'address_line1',
            'address_line2',
            'province',
            'regency',
            'district',
            'village',
            'phone_number',
            'email',
        ]

        labels = {
            'code': 'Warehouse Code *',
            'name': 'Warehouse Name *',
            'location': 'Location *',
            'address_line1': 'Address Line 1',
            'address_line2': 'Address Line 2',
            'phone_number': 'Phone Number',
            'email': 'Email Address',
            'province': 'Province',
            'regency': 'Regency *',
            'district': 'District *',
            'village': 'Village *',
        }

        help_texts = {
            'code': 'A unique code for this warehouse (up to 20 characters).',
            'name': 'Enter the full name of the warehouse.',
            'location': 'Provide a general description of the location within or near the warehouse, e.g., "Zone A".',
            'capacity': 'Enter the maximum storage capacity of this warehouse, e.g., in cubic meters (m³) (optional).',
            'manager': 'Enter the full name of the warehouse manager (optional).',
            'address_line1': 'Enter the primary street address (optional).',
            'address_line2': 'Enter any additional address information (e.g., suite number) (optional).',
            'regency': 'Select the regency or city.',
            'district': 'Select the district.',
            'village': 'Select the village.',
            'phone_number': 'Enter a contact phone number for the warehouse (optional).',
            'email': 'Enter a contact email address for the warehouse (optional).',
            'active': 'Check this box if this warehouse is active.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Iterate through each field and set widget attributes
        for field_name, field in self.fields.items():
        
            if self.errors.get(field_name):
                # Add 'is-invalid' class to fields with errors
                # field.widget.attrs.update({'class': 'form-control parsley-error'})
                field.widget.attrs.update({'class': 'form-control custom-form-control-error'})
            else:
                # Ensure 'form-control' class is present for other fields
                field.widget.attrs.update({'class': 'form-control'})

            # Optionally, add other attributes like autocomplete="off"
            field.widget.attrs.update({'autocomplete': 'off'})


class ProvinsiForm(forms.ModelForm):
    class Meta:
        model = Provinsi
        fields = ['name', 'id_code']

class KabupatenKotaForm(forms.ModelForm):
    class Meta:
        model = KabupatenKota
        fields = ['provinsi', 'name', 'id_code', 'type']

class KecamatanForm(forms.ModelForm):
    class Meta:
        model = Kecamatan
        fields = ['kabupaten_kota', 'name', 'id_code']

class KelurahanDesaForm(forms.ModelForm):
    class Meta:
        model = KelurahanDesa
        fields = ['kecamatan', 'name', 'id_code', 'postal_code']

class AreaForm(forms.ModelForm):
    warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control col-md-7 col-xs-12'})
    )
     
    class Meta:
        model = Area
        fields =  ['warehouse', 'area_name', 'capacity'] 

    # Adding Bootstrap classes to form fields
        widgets = {
            'area_name': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
        }