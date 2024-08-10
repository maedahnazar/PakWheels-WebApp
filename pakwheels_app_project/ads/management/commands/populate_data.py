from datetime import datetime
import json

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from ads.models import Ad
from ads.constants import DEFAULT_UNKNOWN_VALUE
from cars.models import Car, Feature, Image, Source, InspectionReport


User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the database from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        with open(kwargs['json_file'], 'r') as file:
            for ad_entry in json.load(file):     
                ad = self.create_ad(ad_entry, self.create_or_get_user())
                car = self.create_car(ad, ad_entry)
                self.add_features_to_car(car, ad_entry['car_features'])
                self.add_images_to_car(car, ad_entry['images'])
                self.create_inspection_report(car, ad_entry.get('inspection_report', {}))

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))

    def create_or_get_user(self):
        user, created = User.objects.get_or_create(username='pakwheels')

        user.set_password('pakwheels_password')
        user.save(update_fields=['password'] if not created else None)

        return user

    def create_ad(self, ad_entry, user):
        return Ad.objects.create(
            user=user,
            title=ad_entry['title'],
            price = float(
                ad_entry.get('price', '').replace('PKR ', '') 
                if ad_entry.get('price', '').replace('PKR ', '').isdigit() else '0'
            ),
            location=ad_entry['location'],
            seller_comments = '\n'.join(ad_entry.get('seller_comments', []))
        )
    
    def create_car(self, ad, ad_entry):
        return Car.objects.create(
            ad=ad,
            registered_in=ad_entry['car_details'].get('Registered In', DEFAULT_UNKNOWN_VALUE),
            color=ad_entry['car_details'].get('Color', DEFAULT_UNKNOWN_VALUE),
            assembly=ad_entry['car_details'].get('Assembly', DEFAULT_UNKNOWN_VALUE),
            engine_capacity=int(ad_entry['car_details'].get('Engine Capacity', '0').replace(' cc', '') or 0),
            body_type=ad_entry['car_details'].get('Body Type', DEFAULT_UNKNOWN_VALUE)
        )

    def add_features_to_car(self, car, feature_names):
        feature_instances = [
            Feature.objects.get_or_create(name=feature_name.strip())[0]
            for feature_name in feature_names
        ]
        car.features.set(feature_instances)

    def add_images_to_car(self, car, image_urls):
        image_instances = [Image(car=car, external_image_url=image_url) for image_url in image_urls]
        Image.objects.bulk_create(image_instances)

    def create_inspection_report(self, car, report_details):
        if not (report_details and any(report_details.values())):
            self.stdout.write(self.style.WARNING(f'No valid inspection report data for Car: {car}'))
            return

        source, created = Source.objects.get_or_create(name='Pak Wheels')
        
        inspection_report = InspectionReport.objects.create(
            car=car,
            source=source,
            inspected_date = datetime.strptime(report_details.get('Inspected Date', ''), '%m/%d/%y') 
                            if report_details.get('Inspected Date', '') else None,
            overall_rating=report_details.get('Overall Rating', None),
            grade=report_details.get('Grade', None),
            exterior_body=report_details.get('Exterior & Body', None),
            engine_transmission_clutch=report_details.get('Engine/Transmission/Clutch', None),
            suspension_steering=report_details.get('Suspension/Steering', None),
            interior=report_details.get('Interior', None),
            ac_heater=report_details.get('AC/Heater', None)
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created InspectionReport: {inspection_report}'))
