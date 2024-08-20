from cars.models import Car, Image, InspectionReport


class CarService:
    def save_ad_with_related(ad, car_form, image_form, inspection_report_form, user):
        ad.user = user
        ad.save()

        car = car_form.save(commit=False)
        car.ad = ad
        car.save()
        car_form.save_m2m()

        features = car_form.cleaned_data.get('features')
        if features:
            for feature in features:
                car.features.add(feature)

        images_to_create = [
                Image(car=car, uploaded_image=image)
                for image in image_form.cleaned_data['uploaded_images']
            ]
        
        Image.objects.bulk_create(images_to_create)

        inspection_report = inspection_report_form.save(commit=False)
        if inspection_report:
            inspection_report.car = car
            inspection_report.save()
