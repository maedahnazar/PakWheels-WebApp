import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from ads.models import Ad
from ads.api.v3.serializers import AdSerializer, AdCreateUpdateSerializer


class AdListView(ListAPIView):
    queryset = Ad.objects.filter(is_active=True)
    serializer_class = AdSerializer
    pagination_class = PageNumberPagination


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.filter(is_active=True)
    serializer_class = AdSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'ad_id'


class AdCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
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


class AdUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def update_ad(self, request, ad_id):
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

    def put(self, request, ad_id, *args, **kwargs):
        return self.update_ad(request, ad_id)

    def patch(self, request, ad_id, *args, **kwargs):
        return self.update_ad(request, ad_id)


class AdDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, ad_id, *args, **kwargs):
        ad = get_object_or_404(Ad, id=ad_id, user=request.user)
        ad.is_active = False
        ad.save(update_fields=['is_active'])

        car = ad.car
        car.is_active = False
        car.save(update_fields=['is_active'])

        car.images.update(is_active=False)
        car.inspection_reports.update(is_active=False)

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCarsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(AdSerializer(Ad.objects.filter(user=request.user, is_active=True), many=True).data)
