from django import forms
# from .models import Warehouse, Area, Country, State, City
# from .models import Province, Regency, District, Village, Warehouse, Area
from .models import Provinsi, KabupatenKota, Kecamatan, KelurahanDesa, Warehouse, Area

class WarehouseForm(forms.ModelForm):

    # from kodepos.extended.json
    province = forms.ModelChoiceField(
        queryset=Provinsi.objects.all().order_by('name'),
        label='Province',
        help_text='Select the province or state (optional).'
    )

    '''
    # get all wilayah indonesia
    province = forms.ModelChoiceField(
        queryset=Province.objects.all().order_by('name'),
        label='Province',
        help_text='Select the province or state (optional).'
    )'''

    '''
    # get all countries
    country = forms.ModelChoiceField(
        queryset=Country.objects.all().order_by('name'),
        label='Country'
    )
    state = forms.ModelChoiceField(
        queryset=State.objects.none(),
        label='State'
    )
    city = forms.ModelChoiceField(
        queryset=State.objects.none(),
        label='City'
    )
    '''
    class Meta:
        model = Warehouse

        '''
        # get all countries
        fields = [
            'code',
            'name',
            'location',
            'capacity',
            'manager',
            'address_line1',
            'address_line2',
            'country',
            'state',
            'city',
            'postal_code',
            'phone_number',
            'email'
        ]
        '''

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
            'postal_code',
            'phone_number',
            'email'
        ]

        # Adding Bootstrap classes to form fields
        widgets = {
            
            '''
            # get all countries
            'country': forms.Select(attrs={
                'hx-get': "{% url 'htmx_load_states' %}",
                'hx-target': '#id_state',
                'hx-trigger': 'change'
            }),
            'state': forms.Select(attrs={
                'id': 'id_state',  # Ensure this ID is consistent with the HTMX target
                'hx-get': "{% url 'htmx_load_cities' %}",
                'hx-target': '#id_city',
                'hx-trigger': 'change'
            }),
            'city': forms.Select(attrs={'id':'id_city'}),
            '''


        }

        labels = {
            'code': 'Warehouse Code *',
            'name': 'Warehouse Name *',
            'location': 'Location *',
            'capacity': 'Capacity *',
            'address_line1': 'Address Line 1',
            'address_line2': 'Address Line 2',
            'postal_code': 'Postal Code',
            'phone_number': 'Phone Number',
            'email': 'Email Address',
        }

        help_texts = {
            'code': 'A unique code for this warehouse (up to 20 characters).',
            'name': 'Enter the full name of the warehouse.',
            'location': 'Provide a general description of the location within or near the warehouse, e.g., "Zone A".',
            'capacity': 'Enter the maximum storage capacity of this warehouse, e.g., in cubic meters (m³).',
            'manager': 'Enter the full name of the warehouse manager (optional).',
            'address_line1': 'Enter the primary street address (optional).',
            'address_line2': 'Enter any additional address information (e.g., suite number) (optional).',
            'regency': 'Select the regency or city (optional).',
            'district': 'Select the district (optional).',
            'village': 'Select the village (optional).',
            'postal_code': 'Enter the postal or ZIP code (optional).',
            'phone_number': 'Enter a contact phone number for the warehouse (optional).',
            'email': 'Enter a contact email address for the warehouse (optional).',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Iterate through each field and set widget attributes
        for field_name, field in self.fields.items():
            '''if 'province' in self.data:
                try:
                    province_id = int(self.data.get('province'))
                    self.fields['regency'].queryset = Regency.objects.filter(province_id=province_id).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['regency'].queryset = self.instance.province.regencies.order_by('name')
            '''
        
            if self.errors.get(field_name):
                # Add 'is-invalid' class to fields with errors
                # field.widget.attrs.update({'class': 'form-control parsley-error'})
                field.widget.attrs.update({'class': 'form-control custom-form-control-error'})
            else:
                # Ensure 'form-control' class is present for other fields
                field.widget.attrs.update({'class': 'form-control'})

            # Optionally, add other attributes like autocomplete="off"
            field.widget.attrs.update({'autocomplete': 'off'})

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