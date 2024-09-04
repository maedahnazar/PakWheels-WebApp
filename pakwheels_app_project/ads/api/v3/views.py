import json

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ads.models import Ad
from cars.models import Car
from ads.api.v3.serializers import AdSerializer, AdCreateUpdateSerializer, CarSerializer


@api_view(['GET'])
def ad_list_view(request):
    ads = Ad.objects.filter(is_active=True)[:10]  
    serializer = AdSerializer(ads, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def ad_detail_view(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, is_active=True)
    serializer = AdSerializer(ad)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ad_create_view(request):
    car_data = request.data.get('car', {})
    car_data = json.loads(car_data) if isinstance(car_data, str) else car_data

    images = request.FILES.getlist('car[images]')
    car_data['images'] = images

    ad_data = {
        "title": request.data.get("title"),
        "price": request.data.get("price"),
        "location": request.data.get("location"),
        "seller_comments": request.data.get("seller_comments"),
        "user": request.data.get("user"),
        "car": car_data
    }

    serializer = AdCreateUpdateSerializer(data=ad_data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def ad_update_view(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user, is_active=True)
    car_data = request.data.get('car', {})
    car_data = json.loads(car_data) if isinstance(car_data, str) else car_data

    images = request.FILES.getlist('car[images]')
    car_data.setdefault('images', []).extend(images)

    ad_data = {
        "title": request.data.get("title"),
        "price": request.data.get("price"),
        "location": request.data.get("location"),
        "seller_comments": request.data.get("seller_comments"),
        "user": request.data.get("user"),
        "car": car_data
    }

    serializer = AdCreateUpdateSerializer(ad, data=ad_data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def ad_delete_view(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)
    ad.is_active = False
    ad.save()

    car = ad.car
    car.is_active = False
    car.save()

    car.images.update(is_active=False)
    car.inspection_reports.update(is_active=False)

    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_cars_list_view(request):
    ads = Ad.objects.filter(user=request.user, is_active=True)
    serializer = AdSerializer(ads, many=True)
    return Response(serializer.data)
