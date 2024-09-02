import json, os
from django.core.management.base import BaseCommand
from InventoryApp.models import Country, Timezone, State, City

# get all countries
class Command(BaseCommand):
    help = 'Load country data from a JSON file'

    def handle(self, *args, **kwargs):
        # Path to the JSON file
        countries_file_path = os.path.join(
            os.path.dirname(__file__),  # Directory of the current file
            'data_all_countries',                    # Data directory
            'countries.json'           # JSON file name
        )

        states_json_path = os.path.join(
            os.path.dirname(__file__),  # Directory of the current file
            'data_all_countries',                    # Data directory
            'states.json'              # JSON file name for states
        )

        cities_json_path = os.path.join(
            os.path.dirname(__file__),  # Directory of the current file
            'data_all_countries',                    # Data directory
            'cities.json'              # JSON file name for cities
        )
        
        # Load countries
        with open(countries_file_path, 'r') as file:
            data = json.load(file)

            for country_data in data:
                # Handle timezones
                timezones = country_data.pop('timezones', [])
                timezone_objects = []

                if timezones:
                    for tz in timezones:
                        tz_obj, created = Timezone.objects.update_or_create(
                            zone_name=tz['zoneName'],
                            defaults={
                                'gmt_offset': tz['gmtOffset'],
                                'gmt_offset_name': tz['gmtOffsetName'],
                                'abbreviation': tz['abbreviation'],
                                'tz_name': tz['tzName']
                            }
                        )
                        timezone_objects.append(tz_obj)
                
                # Handle country
                country, created = Country.objects.update_or_create(
                    id=country_data['id'],
                    defaults={
                        'name': country_data['name'],
                        'iso3': country_data['iso3'],
                        'iso2': country_data['iso2'],
                        'numeric_code': country_data['numeric_code'],
                        'phone_code': country_data['phone_code'],
                        'capital': country_data['capital'],
                        'currency': country_data['currency'],
                        'currency_name': country_data['currency_name'],
                        'currency_symbol': country_data['currency_symbol'],
                        'tld': country_data['tld'],
                        'native': country_data['native'],
                        'region': country_data['region'],
                        'region_id': country_data['region_id'],
                        'subregion': country_data['subregion'],
                        'subregion_id': country_data['subregion_id'],
                        'nationality': country_data['nationality'],
                    }
                )
                
                # Add timezones to the country
                country.timezones.set(timezone_objects)

        # Load states
        with open(states_json_path, 'r') as file:
            state_data = json.load(file)

            for state_data_item in state_data:
                country = Country.objects.filter(id=state_data_item['country_id']).first()
                if country:
                    State.objects.update_or_create(
                        id=state_data_item['id'],
                        defaults={
                            'name': state_data_item['name'],
                            'country': country,
                            'country_code': state_data_item['country_code'],
                            'country_name': state_data_item['country_name'],
                            'state_code': state_data_item['state_code'],
                            'type': state_data_item.get('type'),
                            'latitude': state_data_item['latitude'],
                            'longitude': state_data_item['longitude']
                        }
                    )

        with open(cities_json_path, 'r') as file:
            city_data = json.load(file)
            
            for city_data_item in city_data:
                state = State.objects.filter(id=city_data_item['state_id']).first()
                if state:
                    City.objects.update_or_create(
                        id=city_data_item['id'],
                        defaults={
                            'name': city_data_item['name'],
                            'state': state,
                            'latitude': city_data_item['latitude'],
                            'longitude': city_data_item['longitude'],
                            'state_code': city_data_item.get('state_code'),
                            'state_name': city_data_item.get('state_name'),
                            'country_code': city_data_item.get('country_code'),
                            'country_name': city_data_item.get('country_name'),
                            'wikiDataId': city_data_item.get('wikiDataId'),
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Successfully loaded country and state data'))
