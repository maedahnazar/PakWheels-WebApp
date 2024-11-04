import json

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from ads.models import Ad
from cars.models import Car
from ads.api.v3.serializers import AdSerializer, AdCreateUpdateSerializer, CarSerializer


@api_view(['GET'])
def ad_list_view(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10

    return paginator.get_paginated_response(
        AdSerializer(paginator.paginate_queryset(Ad.objects.filter(is_active=True), request), many=True).data
    )

@api_view(['GET'])
def ad_detail_view(request, ad_id):
    return Response(AdSerializer(get_object_or_404(Ad, id=ad_id, is_active=True)).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ad_create_view(request):
    car_details = request.data.get('car', {})
    car_details = json.loads(car_details) if isinstance(car_details, str) else car_details

    car_details['images'] = request.FILES.getlist('car[images]')

    serializer = AdCreateUpdateSerializer(
        data={
            "title": request.data.get("title"),
            "price": request.data.get("price"),
            "location": request.data.get("location"),
            "seller_comments": request.data.get("seller_comments"),
            "user": request.data.get("user"),
            "car": car_details
        })

    return Response(
        serializer.data if serializer.is_valid() and serializer.save(user=request.user) else serializer.errors,
        status=status.HTTP_201_CREATED if serializer.is_valid() else status.HTTP_400_BAD_REQUEST
    )

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def ad_update_view(request, ad_id):
    car_details = request.data.get('car', {})
    car_details = json.loads(car_details) if isinstance(car_details, str) else car_details

    car_details.setdefault('images', []).extend(request.FILES.getlist('car[images]'))

    serializer = AdCreateUpdateSerializer(
        get_object_or_404(Ad, id=ad_id, user=request.user, is_active=True),
        data={
            "title": request.data.get("title"),
            "price": request.data.get("price"),
            "location": request.data.get("location"),
            "seller_comments": request.data.get("seller_comments"),
            "user": request.data.get("user"),
            "car": car_details
        },
        partial=True
    )

    return Response(
        serializer.data if serializer.is_valid() and serializer.save() else serializer.errors,
        status=status.HTTP_201_CREATED if serializer.is_valid() else status.HTTP_400_BAD_REQUEST
    )

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def ad_delete_view(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)
    ad.is_active = False
    ad.save(update_fields=['is_active'])

    car = ad.car
    car.is_active = False
    car.save(update_fields=['is_active'])

    car.images.update(is_active=False)
    car.inspection_reports.update(is_active=False)

    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_cars_list_view(request):
    return Response(AdSerializer(Ad.objects.filter(user=request.user, is_active=True), many=True).data)
