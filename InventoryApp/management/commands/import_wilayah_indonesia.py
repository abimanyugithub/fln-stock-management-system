import json, os
from django.core.management.base import BaseCommand
from InventoryApp.models import Province, Regency, District, Village

class Command(BaseCommand):
    help = 'Import regions from a JSON file'

    def handle(self, *args, **kwargs):
        # Path to the JSON file
        provinces_file_path = os.path.join(
            os.path.dirname(__file__),  # Directory of the current file
            'data_indonesia',  # Data directory
            'provinces.json' # JSON file name
        )

        regencies_file_path = os.path.join(
            os.path.dirname(__file__),  # Directory of the current file
            'data_indonesia',  # Data directory
            'regencies.json' # JSON file name
        )

        district_file_path = os.path.join(
            os.path.dirname(__file__),  # Directory of the current file
            'data_indonesia',  # Data directory
            'districts.json' # JSON file name
        )

        village_file_path = os.path.join(
            os.path.dirname(__file__),  # Directory of the current file
            'data_indonesia',  # Data directory
            'villages.json' # JSON file name
        )

        # Read and load province data
        with open(provinces_file_path, 'r') as file:
            data_province = json.load(file)

        # Iterate over the JSON data and create Province objects
        for item in data_province:
            Province.objects.update_or_create(
                id=item['id'],
                defaults={
                    'name': item['name'],
                    'alt_name': item.get('alt_name', ''),
                    'latitude': item['latitude'],
                    'longitude': item['longitude']
                }
            )

            self.stdout.write(self.style.SUCCESS(f'Province "{item["name"]}" processed.'))

        # Read and load regency data
        with open(regencies_file_path, 'r') as file:
            data_regency = json.load(file)

        # Iterate over the JSON data and create Regency objects
        for item in data_regency:
            province_id = item['province_id']

            try:
                province = Province.objects.get(id=province_id)
            except Province.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Province with ID "{province_id}" does not exist. Skipping regency.'))
                continue
            
            Regency.objects.update_or_create(
                id=item['id'],
                defaults={
                    'province': province,
                    'name': item['name'],
                    'alt_name': item.get('alt_name', ''),
                    'latitude': item['latitude'],
                    'longitude': item['longitude']
                }
            )

            self.stdout.write(self.style.SUCCESS(f'Regency "{item["name"]}" processed.'))

        # Read and load district data
        with open(district_file_path, 'r') as file:
            data_district = json.load(file)

        # Iterate over the JSON data and create Regency objects
        for item in data_district:
            regency_id = item['regency_id']

            try:
                regency = Regency.objects.get(id=regency_id)
            except Regency.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Regency with ID "{regency_id}" does not exist. Skipping district.'))
                continue
            
            District.objects.update_or_create(
                id=item['id'],
                defaults={
                    'regency': regency,
                    'name': item['name'],
                    'alt_name': item.get('alt_name', ''),
                    'latitude': item['latitude'],
                    'longitude': item['longitude']
                }
            )
        
            self.stdout.write(self.style.SUCCESS(f'District "{item["name"]}" processed.'))

        # Read and load village data
        with open(village_file_path, 'r') as file:
            data_village = json.load(file)

        # Iterate over the JSON data and create Village objects
        for item in data_village:
            district_id = item['district_id']

            try:
                district = District.objects.get(id=district_id)
            except District.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'District with ID "{district_id}" does not exist. Skipping district.'))
                continue
            
            Village.objects.update_or_create(
                id=item['id'],
                defaults={
                    'district': district,
                    'name': item['name'],
                    'latitude': item['latitude'],
                    'longitude': item['longitude']
                }
            )
        
            self.stdout.write(self.style.SUCCESS(f'Village "{item["name"]}" processed.'))


