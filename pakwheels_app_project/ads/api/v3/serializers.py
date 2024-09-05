from rest_framework import serializers

from ads.models import Ad
from cars.models import Car, Feature, Image, InspectionReport, CarFeatureThrough


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'created_at', 'modified_at', 'name', 'is_active']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'created_at', 'modified_at', 'uploaded_image', 'is_active']


class InspectionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionReport
        fields = [
            'id', 
            'created_at', 
            'modified_at', 
            'inspected_date', 
            'overall_rating', 
            'grade',
            'exterior_body',
            'engine_transmission_clutch',
            'suspension_steering',
            'interior',
            'ac_heater',
            'is_active'
        ]


class CarSerializer(serializers.ModelSerializer):
    features = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Car
        fields = ['registered_in', 'color', 'assembly', 'engine_capacity', 'body_type', 'features', 'images']

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

        for existing_image in list(instance.images.all()):
            if existing_image.uploaded_image not in images_files:
                existing_image.is_active = False
                existing_image.save()

        for image_file in images_files:
            if not instance.images.filter(uploaded_image=image_file).exists():
                Image.objects.create(car=instance, uploaded_image=image_file)

        return instance


class AdSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = Ad
        fields = ['id', 'title', 'price', 'location', 'is_active', 'car']


class AdCreateUpdateSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = Ad
        fields = "__all__"

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
