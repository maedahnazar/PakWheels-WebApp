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
        with open(kwargs['json_file'], 'r') as file:
            user = self.create_or_get_user()
            for ad_entry in json.load(file):
                ad = self.create_ad(ad_entry, user)
                car = self.create_car(ad, ad_entry)
                self.add_features_to_car(car, ad_entry['car_features'])
                self.add_images_to_car(car, ad_entry['images'])
                self.create_inspection_report(car, ad_entry.get('inspection_report', {}))

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))

    def create_or_get_user(self):
        user, created = User.objects.get_or_create(username='pakwheels')
        user.set_password('pakwheels_password')
        user.save()

        return user

    def create_ad(self, ad_entry, user):
        price = self.parse_price(ad_entry.get('price', ''))

        return Ad.objects.create(
            user=user,
            title=ad_entry['title'],
            price=price,
            location=ad_entry['location'],
            seller_comments=', '.join(ad_entry.get('seller_comments', []))
        )

    def parse_price(self, price_value):
        cleaned_price = price_value.replace('PKR ', '').replace(',', '') 
        
        try:
            price = float(cleaned_price)
        except ValueError:
            price = 0.0

        return price


    def create_car(self, ad, ad_entry):
        last_updated = self.parse_date(ad_entry.get('Last Updated:', None))

        return Car.objects.create(
            ad=ad,
            registered_in=ad_entry.get('Registered In', 'Unknown'),
            color=ad_entry.get('Color', 'Unknown'),
            assembly=ad_entry.get('Assembly', 'Unknown'),
            engine_capacity=self.parse_engine_capacity(ad_entry.get('Engine Capacity', '0')),
            body_type=ad_entry.get('Body Type', 'Unknown'),
            last_updated=last_updated
        )

    def parse_date(self, date_str):
        return datetime.strptime(date_str, '%b %d, %Y') if date_str else None

    def parse_engine_capacity(self, engine_capacity):
        cleaned_engine_capacity = engine_capacity.replace(' cc', '')

        try:
            capacity = int(cleaned_engine_capacity)
        except ValueError:
            capacity = 0

        return capacity

    def add_features_to_car(self, car, feature_names):
        for feature_name in feature_names:
            feature, created = Feature.objects.get_or_create(name=feature_name.strip())
            car.features.add(feature)

    def add_images_to_car(self, car, image_urls):
        for image_url in image_urls:
            Image.objects.create(
                car=car,
                image_url=image_url
            )

    def create_inspection_report(self, car, inspection_data):
        if inspection_data and any(inspection_data.values()):
            source, created = Source.objects.get_or_create(name='Pak Wheels')
            inspected_date = self.parse_date(inspection_data.get('inspected_date', None))

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
            self.stdout.write(self.style.WARNING(f'No valid inspection report data for Ad: {Ad.title}'))
