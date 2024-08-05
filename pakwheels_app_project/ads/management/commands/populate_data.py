import json
from datetime import datetime
from django.core.management.base import BaseCommand
from ads.models import Ad
from cars.models import Car, Feature, Image, Source, InspectionReport
from users.models import User

class Command(BaseCommand):
    help = 'Populate the database from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        with open(json_file, 'r') as file:
            ads_data = json.load(file)

            # Assuming a single user for simplicity; modify as needed for multiple users
            user, created = User.objects.get_or_create(username='default_user')
            user.set_password('default_password')
            user.save()

            for data in ads_data:
                # Handle price field
                price_str = data['price'].replace('PKR ', '').replace(',', '')
                try:
                    price = float(price_str)
                except ValueError:
                    price = 0.0  # Set default price when conversion fails

                ad = Ad.objects.create(
                    user=user,
                    title=data['title'],
                    price=price,
                    location=data['location'],
                    seller_comments=' '.join(data['seller_comments'])
                )

                car_data = data['car_details']
                last_updated_str = car_data.get('Last Updated:', None)
                if last_updated_str:
                    last_updated = datetime.strptime(last_updated_str, '%b %d, %Y')
                else:
                    last_updated = None

                car = Car.objects.create(
                    ad=ad,
                    registered_in=car_data.get('Registered In', 'Unknown'),
                    color=car_data.get('Color', 'Unknown'),
                    assembly=car_data.get('Assembly', 'Unknown'),
                    engine_capacity=int(car_data.get('Engine Capacity', '0').replace(' cc', '')),
                    body_type=car_data.get('Body Type', 'Unknown'),
                    last_updated=last_updated
                )

                for feature_name in data['car_features']:
                    feature, created = Feature.objects.get_or_create(name=feature_name.strip())
                    car.features.add(feature)

                for image_url in data['images']:
                    Image.objects.create(
                        car=car,
                        image_url=image_url
                    )

                # Handle inspection reports
                inspection_data = data.get('inspection_report', {})
                if inspection_data and any(inspection_data.values()):  # Check if there's any non-empty value
                    source_name = 'Pak Wheels'
                    source, created = Source.objects.get_or_create(name=source_name)

                    inspected_date_str = inspection_data.get('inspected_date', None)
                    if inspected_date_str:
                        inspected_date = datetime.strptime(inspected_date_str, '%b %d, %Y')
                    else:
                        inspected_date = None

                    inspection_report = InspectionReport.objects.create(
                        car=car,
                        source=source,
                        inspected_date=inspected_date,
                        overall_rating=inspection_data.get('overall_rating', None),
                        grade=inspection_data.get('grade', None),
                        exterior_body=inspection_data.get('exterior_body', None),
                        engine_transmission_clutch=inspection_data.get('engine_transmission_clutch', None),
                        suspension_steering=inspection_data.get('suspension_steering', None),
                        interior=inspection_data.get('interior', None),
                        ac_heater=inspection_data.get('ac_heater', None)
                    )

                    self.stdout.write(self.style.SUCCESS(f'Successfully created InspectionReport: {inspection_report}'))
                else:
                    self.stdout.write(self.style.WARNING(f'No valid inspection report data for Ad: {ad.title}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
