from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
'''
# get all countries https://github.com/dr5hn/countries-states-cities-database
class Timezone(models.Model):
    zone_name = models.CharField(max_length=255)
    gmt_offset = models.IntegerField()
    gmt_offset_name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=10)
    tz_name = models.CharField(max_length=100)

    def __str__(self):
        return self.zone_name

class Country(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    iso3 = models.CharField(max_length=3)
    iso2 = models.CharField(max_length=2)
    numeric_code = models.CharField(max_length=3)
    phone_code = models.CharField(max_length=15)
    capital = models.CharField(max_length=255)
    currency = models.CharField(max_length=10)
    currency_name = models.CharField(max_length=255)
    currency_symbol = models.CharField(max_length=10)
    tld = models.CharField(max_length=10)
    native = models.CharField(max_length=255,blank=True, null=True)
    region = models.CharField(max_length=50)
    region_id = models.CharField(max_length=10, blank=True, null=True)
    subregion = models.CharField(max_length=50)
    subregion_id = models.CharField(max_length=10, blank=True, null=True)
    nationality = models.CharField(max_length=50)
    timezones = models.ManyToManyField(Timezone)

    def __str__(self):
        return self.name
    
class State(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
    country_code = models.CharField(max_length=3)
    country_name = models.CharField(max_length=255)
    state_code = models.CharField(max_length=10)
    type = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.country_name})'
    
class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    latitude = models.CharField(max_length=15, blank=True, null=True)
    longitude = models.CharField(max_length=15, blank=True, null=True)
    # Optional fields
    state_code = models.CharField(max_length=10, blank=True, null=True)
    state_name = models.CharField(max_length=100, blank=True, null=True)
    country_code = models.CharField(max_length=3, blank=True, null=True)
    country_name = models.CharField(max_length=100, blank=True, null=True)
    wikiDataId = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
'''

'''
# get all indonesia https://github.com/yusufsyaifudin/wilayah-indonesia
class Province(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    alt_name = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name
    
class Regency(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='regencies')
    name = models.CharField(max_length=100)
    alt_name = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name
    
class District(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    regency = models.ForeignKey(Regency, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)
    alt_name = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Village(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return self.name'''

class Provinsi(models.Model):
    name = models.CharField(max_length=255, unique=True)
    id_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class KabupatenKota(models.Model):
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE, related_name='kabupaten_kota')
    name = models.CharField(max_length=255)
    id_code = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=50)  # e.g., 'Kabupaten' or 'Kota'

    def __str__(self):
        return self.name


class Kecamatan(models.Model):
    kabupaten_kota = models.ForeignKey(KabupatenKota, on_delete=models.CASCADE, related_name='kecamatan')
    name = models.CharField(max_length=255)
    id_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
    

class KelurahanDesa(models.Model):
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE, related_name='kelurahan_desa')
    name = models.CharField(max_length=255)
    id_code = models.CharField(max_length=20, unique=True)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    code = models.CharField(max_length=20, unique=True)  # unique=True memastikan bahwa tidak ada dua entri
    name = models.CharField(max_length=255) 
    location = models.CharField(max_length=255)
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
    def __str__(self):
        return self.name
    

class Area(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='areas')
    area_name = models.CharField(max_length=255)  # Nama area di dalam warehouse
    capacity = models.PositiveIntegerField()  # Kapasitas maksimum area
    current_inventory = models.PositiveIntegerField(default=0)  # Jumlah inventaris saat ini di area ini

    def __str__(self):
        return f"{self.area_name} ({self.warehouse.name})"
    

class Location(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='locations')
    location_name = models.CharField(max_length=255)  # Nama lokasi di dalam area
    description = models.TextField(blank=True, null=True)  # Deskripsi lokasi (opsional)
    capacity = models.PositiveIntegerField()  # Kapasitas maksimum lokasi
    current_inventory = models.PositiveIntegerField(default=0)  # Jumlah inventaris saat ini di lokasi ini

    def __str__(self):
        return f"{self.location_name} ({self.area.area_name})"