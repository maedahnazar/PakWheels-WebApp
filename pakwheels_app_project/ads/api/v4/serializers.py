from rest_framework import serializers

from ads.models import Ad
from cars.models import Car, Feature, Image, InspectionReport, CarFeatureThrough


class FeatureSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField()
    name = serializers.TextField()
    is_active = serializers.BooleanField()


class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField()
    uploaded_image = serializers.ImageField()
    is_active = serializers.BooleanField()


class InspectionReportSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField()
    inspected_date = serializers.DateField()
    overall_rating = serializers.TextField()
    grade = serializers.TextField()
    exterior_body = serializers.TextField()
    engine_transmission_clutch = serializers.TextField()
    suspension_steering = serializers.TextField()
    interior = serializers.TextField()
    ac_heater = serializers.TextField()
    is_active = serializers.BooleanField()


class CarSerializer(serializers.Serializer):
    registered_in = serializers.TextField()
    color = serializers.TextField()
    assembly = serializers.TextField()
    engine_capacity = serializers.TextField()
    body_type = serializers.TextField()

    features = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    def create(self, validated_data):
        features_ids = validated_data.pop('features', [])
        images_files = validated_data.pop('images', [])

        car = Car.objects.create(**validated_data)

        for feature_id in features_ids:
            CarFeatureThrough.objects.create(car=car, feature_id=feature_id)

        for image_file in images_files:
            Image.objects.create(car=car, uploaded_image=image_file)

        return car

    def update(self, instance, validated_data):
        features_ids = validated_data.pop('features', [])
        images_files = validated_data.pop('images', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.features.clear()
        for feature_id in features_ids:
            CarFeatureThrough.objects.create(car=instance, feature_id=feature_id)

        current_images = {image.uploaded_image.name: image for image in instance.images.all()}
        updated_image_names = {image_file.name for image_file in images_files}

        for image_name, existing_image in current_images.items():
            if image_name not in updated_image_names:
                existing_image.is_active = False
                existing_image.save(update_fields=['is_active'])

        for image_file in images_files:
            if image_file.name not in current_images:
                Image.objects.create(car=instance, uploaded_image=image_file)

        return instance


class AdSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.TextField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    location = serializers.TextField()
    is_active = serializers.BooleanField()

    car = CarSerializer()


class AdCreateUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.TextField()
    price = serializers.TextField()
    location = serializers.TextField()
    seller_comments = serializers.TextField()
    is_active = serializers.BooleanField(required=False)

    user = serializers.IntegerField()
    car = CarSerializer()

    def create(self, validated_data):
        car_data = validated_data.pop('car', None)

        ad = Ad.objects.create(**validated_data)

        if car_data:
            car_serializer = CarSerializer(data=car_data)
            car_serializer.is_valid(raise_exception=True)
            car_serializer.save(ad=ad)

        return ad

    def update(self, instance, validated_data):
        car_data = validated_data.pop('car', None)

        ad = super().update(instance, validated_data)

        if car_data:
            car_serializer = CarSerializer(instance=ad.car, data=car_data)
            car_serializer.is_valid(raise_exception=True)
            car_serializer.save()

        return ad
