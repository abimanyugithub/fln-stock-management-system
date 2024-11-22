import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.forms import ValidationError
import random
import string

# Create your models here.
class Provinsi(models.Model):
    name = models.CharField(max_length=255, unique=True)
    id_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class KabupatenKota(models.Model):
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE, related_name='kabupaten_kota')
    name = models.CharField(max_length=255)
    id_code = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=50)  # e.g., 'Kabupaten' or 'Kota'

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Kecamatan(models.Model):
    kabupaten_kota = models.ForeignKey(KabupatenKota, on_delete=models.CASCADE, related_name='kecamatan')
    name = models.CharField(max_length=255)
    id_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
    

class KelurahanDesa(models.Model):
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE, related_name='kelurahan_desa')
    name = models.CharField(max_length=255)
    id_code = models.CharField(max_length=20, unique=True)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Warehouse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier
    code = models.CharField(max_length=20)  # unique=True memastikan bahwa tidak ada dua entri
    name = models.CharField(max_length=255) 
    zone = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(blank=True, null=True) # Kapasitas maksimum warehouse
    manager = models.CharField(max_length=255, blank=True, null=True)  # Nama manajer gudang
    current_inventory = models.PositiveIntegerField(default=0)  # Jumlah inventaris saat ini
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Alamat Baris 1')
    address_line2 = models.CharField(max_length=255, blank=True, null=True, verbose_name='Alamat Baris 2')
    province = models.ForeignKey(Provinsi, on_delete=models.CASCADE, blank=True, null=True)
    regency = models.ForeignKey(KabupatenKota, on_delete=models.CASCADE)
    district = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    village = models.ForeignKey(KelurahanDesa, on_delete=models.CASCADE)

    '''
    province = models.ForeignKey(Province, on_delete=models.CASCADE, blank=True, null=True)
    regency = models.ForeignKey(Regency, on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, blank=True, null=True)
    '''

    '''
    # get all countries
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    '''

    # postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='Kode Pos')
    # phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Nomor Telepon')
    email = models.EmailField(max_length=254, blank=True, null=True, verbose_name='Alamat Email')
    phone_number = models.CharField(
        max_length=15,  # Adjust the length as needed
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        blank=True,  # Set to False if the phone number is required
        null=True    # Set to False if the phone number cannot be null
    )
    '''postal_code = models.CharField(
        max_length=10,  # Adjust the length as needed
        validators=[
            RegexValidator(
                regex=r'^\d{5}(-\d{4})?$',
                message="Enter a valid postal code. For example, '12345' or '12345-6789'."
            )
        ],
        blank=True,  # Set to False if the postal code is required
        null=True    # Set to False if the postal code cannot be null
    )
    '''
    def clean(self):
        # Jika active True, periksa apakah code sudah ada
        if self.active:
            if Warehouse.objects.exclude(pk=self.pk).filter(code=self.code, active=True).exists():
                raise ValidationError(f'The code "{self.code}" must be unique when active.')

    def __str__(self):
        return f"{self.code} ({self.name})"
    

    class Meta:
        ordering = ['code']
    

class Area(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='areas')
    area_name = models.CharField(max_length=255)  # Nama area di dalam warehouse
    capacity = models.PositiveIntegerField(blank=True, null=True)  # Kapasitas maksimum area
    current_inventory = models.PositiveIntegerField(default=0)  # Jumlah inventaris saat ini di area ini
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.area_name} ({self.warehouse.name})"
    
    class Meta:
        ordering = ['area_name']


class Location(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='locations')
    location_name = models.CharField(max_length=255)  # Nama lokasi di dalam area
    description = models.TextField(blank=True, null=True)  # Deskripsi lokasi (opsional)
    capacity = models.PositiveIntegerField()  # Kapasitas maksimum lokasi
    current_inventory = models.PositiveIntegerField(default=0)  # Jumlah inventaris saat ini di lokasi ini

    def __str__(self):
        return f"{self.location_name} ({self.area.area_name})"
    
    
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

'''class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    # stock_quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['code']'''

class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    supplier_code = models.CharField(max_length=100, unique=True, blank=True)  # Supplier Code
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UOM(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10)  # For example, kg, l, m
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} ({self.name})"
    
    
class ProductType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True) 
    code = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} ({self.name})"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    # suppliers = models.ManyToManyField(Supplier, related_name='products')  # Many-to-many relationship
    uom = models.ForeignKey(UOM, on_delete=models.CASCADE, related_name='products')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products')
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def generate_sku(self):
        """Generate a random SKU string of length 10 (you can adjust this length)."""
        return ''.join(random.choices('0123456789', k=10))  # Menghasilkan angka acak

    def save(self, *args, **kwargs):
        if not self.sku:  # Jika SKU tidak diisi, maka akan digenerate
            self.sku = self.generate_sku()

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name