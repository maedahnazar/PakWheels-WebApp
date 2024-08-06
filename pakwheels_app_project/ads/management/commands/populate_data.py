import json
from datetime import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from ads.models import Ad
from cars.models import Car, Feature, Image, Source, InspectionReport


class Command(BaseCommand):
    help = 'Populate the database from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        with open(kwargs['json_file'], 'r') as file:
            for ad_entry in json.load(file):
                user = self.create_or_get_user()
                ad = self.create_ad(ad_entry, user)
                car = self.create_car(ad, ad_entry)
                self.add_features_to_car(car, ad_entry['car_features'])
                self.add_images_to_car(car, ad_entry['images'])
                self.create_inspection_report(car, ad_entry.get('inspection_report', {}))

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))

    def create_or_get_user(self):
        User = get_user_model()
        user, created = User.objects.get_or_create(username='pakwheels')

        if created:
            user.set_password('pakwheels_password')
            user.save()
        else:
            user.set_password('pakwheels_password')
            user.save(update_fields=['password'])

        return user

    def create_ad(self, ad_entry, user):
        return Ad.objects.create(
            user=user,
            title=ad_entry['title'],
            price=self.parse_price(ad_entry.get('price', '')),
            location=ad_entry['location'],
            seller_comments=', '.join(ad_entry.get('seller_comments', []))
        )

    def parse_price(self, price_value):
        return float(price_value.replace('PKR ', '').replace(',', '') or 0.0)

    def create_car(self, ad, ad_entry):
        return Car.objects.create(
            ad=ad,
            registered_in=ad_entry.get('Registered In', 'Unknown'),
            color=ad_entry.get('Color', 'Unknown'),
            assembly=ad_entry.get('Assembly', 'Unknown'),
            engine_capacity=self.parse_engine_capacity(ad_entry.get('Engine Capacity', '0')),
            body_type=ad_entry.get('Body Type', 'Unknown')
        )

    def parse_date(self, date_str):
        return datetime.strptime(date_str, '%b %d, %Y') if date_str else None

    def parse_engine_capacity(self, engine_capacity):
        return int(engine_capacity.replace(' cc', '') or 0)

    def add_features_to_car(self, car, feature_names):
        feature_instances = [
            Feature.objects.get_or_create(name=feature_name.strip())[0]
            for feature_name in feature_names
        ]
        
        car.features.set(feature_instances)

    def add_images_to_car(self, car, image_urls):
        image_instances = [Image(car=car, external_image_url=image_url) for image_url in image_urls]
        Image.objects.bulk_create(image_instances)

    def create_inspection_report(self, car, inspection_data):
        if not (inspection_data and any(inspection_data.values())):
            self.stdout.write(self.style.WARNING(f'No valid inspection report data for Car: {car}'))
            return

        source, created = Source.objects.get_or_create(name='Pak Wheels')

        inspection_report = InspectionReport.objects.create(
            car=car,
            source=source,
            inspected_date=self.parse_date(inspection_data.get('inspected_date', None)),
            overall_rating=inspection_data.get('overall_rating', None),
            grade=inspection_data.get('grade', None),
            exterior_body=inspection_data.get('exterior_body', None),
            engine_transmission_clutch=inspection_data.get('engine_transmission_clutch', None),
            suspension_steering=inspection_data.get('suspension_steering', None),
            interior=inspection_data.get('interior', None),
            ac_heater=inspection_data.get('ac_heater', None)
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created InspectionReport: {inspection_report}'))
