from django import forms
# from .models import Warehouse, Area, Country, State, City
# from .models import Province, Regency, District, Village, Warehouse, Area
from .models import Provinsi, KabupatenKota, Kecamatan, KelurahanDesa, Warehouse, Area, Category, Product, UOM, ProductType

class WarehouseForm(forms.ModelForm):

    class Meta:
        model = Warehouse
        fields = [
            'code',
            'name',
            'zone',
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
            'zone': 'Zone *',
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
            'zone': 'Provide a general description of the zone within or near the warehouse, e.g., "Zone A".',
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
     
    class Meta:
        model = Area
        fields =  ['warehouse', 'area_name', 'capacity'] 

        # Adding Bootstrap classes to form fields
        widgets = {
            'warehouse': forms.Select(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'area_name': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
        }
        labels = {
            'warehouse': 'Warehouse *',
            'area_name': 'Area *',
        }
        help_texts = {
            'area_name': 'Provide a unique name for the area.',
            'capacity': 'Enter the maximum capacity of the area in units.',
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Sort categories alphabetically in the dropdown
        self.fields['warehouse'].queryset = Warehouse.objects.all().order_by('code')


class UOMForm(forms.ModelForm):
    class Meta:
        model = UOM
        fields = [
            'name',
            'code',
            'description',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'code': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'description': forms.Textarea(attrs={'class': 'form-control col-md-7 col-xs-12'}),
        }

        help_texts = {
            'name': 'Enter the name of the unit of measurement (e.g., Kilogram, Liter, Meter). This should be unique.',
            'description': 'Provide a detailed description of the unit of measurement (optional). This can include the usage or details about the unit.',
            'code': 'Enter the unit’s code (e.g., kg for kilogram, l for liter). This will be used for shorthand representation.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Iterate through each field and set widget attributes
        for field_name, field in self.fields.items():
            # Set autocomplete="off" for each field's widget
            field.widget.attrs.update({'autocomplete': 'off'})

class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = [
            'name',
            'code',
            'description',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'code': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'description': forms.Textarea(attrs={'class': 'form-control col-md-7 col-xs-12'}),
        }

        help_texts = {
            'name': 'Enter a unique name for the product type (e.g., Raw Materials, Finished Goods).',
            'code': 'Enter a code for the product type (e.g., "RM" for Raw Materials, "FG" for Finished Goods)',
            'description': 'Provide an optional description of the product type.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Iterate through each field and set widget attributes
        for field_name, field in self.fields.items():
            # Set autocomplete="off" for each field's widget
            field.widget.attrs.update({'autocomplete': 'off'})


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = [
            'name',
            'description',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'description': forms.Textarea(attrs={'class': 'form-control col-md-7 col-xs-12'}),
        }

        help_texts = {
            'name': 'Enter the name of the product category.',
            'description': 'Provide a detailed description of the category.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Iterate through each field and set widget attributes
        for field_name, field in self.fields.items():
            # Set autocomplete="off" for each field's widget
            field.widget.attrs.update({'autocomplete': 'off'})


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'product_type', 'category', 'uom', 'description']  # Include other fields if needed

        labels = {
            'sku': 'Code *',
            'name': 'Name *',
            'category': 'Category *',
            'product_type': 'Product Type *',
            'uom': 'UOM *'
        }

        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'name': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'description': forms.Textarea(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'product_type': forms.Select(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'uom': forms.Select(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'category': forms.Select(attrs={'class': 'form-control col-md-7 col-xs-12'}),
        }

        help_texts = {
            'category': 'Select the product category.',
            'name': 'The name of the product being added.',
            'description': 'A detailed description of the product (optional).',
            # 'price': 'The price of the product. Leave blank if unknown.',
            # 'stock_quantity': 'The number of items available in stock.',
            'uom': 'Select the unit of measurement for this product.',
            'product_type': 'Choose the type of product.',
            'suppliers': 'Select the suppliers that provide this product.',
            'sku': 'A unique code for the product. It will be generated automatically if left blank.'
        }
