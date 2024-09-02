from django import forms
from .models import Warehouse, Area, Country, State, City

class WarehouseForm(forms.ModelForm):
    '''country = forms.ModelChoiceField(
        queryset=Country.objects.all().order_by('name'),
        label='Country'
    )
    state = forms.ModelChoiceField(
        queryset=State.objects.all().order_by('name'),
        label='State'
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all().order_by('name'),
        label='City'
    )'''
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
            'country',
            'state',
            'city',
            'postal_code',
            'phone_number',
            'email'
        ]

        # Adding Bootstrap classes to form fields
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control '}),
            'name': forms.TextInput(attrs={'class': 'form-control '}),
            'location': forms.TextInput(attrs={'class': 'form-control '}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control '}),
            'manager': forms.TextInput(attrs={'class': 'form-control '}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control '}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control '}),
            'country': forms.Select(attrs={
                'hx-get': "{% url 'htmx_load_states' %}",
                'hx-target': '#id_state',
                'hx-trigger': 'change'
            }),
            'state': forms.Select(attrs={'id':'id_state',
                'hx-get': "{% url 'htmx_load_cities' %}",
                'hx-target': '#id_city',
                'hx-trigger': 'change'
            }),
            'city': forms.Select(attrs={'id':'id_city'}),
            # 'city': forms.TextInput(attrs={'class': 'form-control '}),
            # 'state': forms.TextInput(attrs={'class': 'form-control '}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control '}),
            # 'country': forms.TextInput(attrs={'class': 'form-control '}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control '}),
            'email': forms.EmailInput(attrs={'class': 'form-control '}),
        }

        labels = {
            'code': 'Warehouse Code *',
            'name': 'Warehouse Name *',
            'location': 'Location *',
            'capacity': 'Capacity *',
            'address_line1': 'Address Line 1',
            'address_line2': 'Address Line 2',
            'city': 'City',
            'state': 'State',
            'postal_code': 'Postal Code',
            'country': 'Country',
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
            'city': 'Enter the city where the warehouse is located (optional).',
            'state': 'Enter the state or province (optional).',
            'postal_code': 'Enter the postal or ZIP code (optional).',
            'country': 'Enter the country where the warehouse is located (optional).',
            'phone_number': 'Enter a contact phone number for the warehouse (optional).',
            'email': 'Enter a contact email address for the warehouse (optional).',
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