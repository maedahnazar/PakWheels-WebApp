from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from ads.forms import AdForm, CarForm, ImageForm, InspectionReportForm
from ads.models import Ad
from cars.models import Image, Car


class AdListView(View):
    def get(self, request):
        ads = Ad.objects.all()

        filters = {
            'title__icontains': request.GET.get('title'),
            'location__icontains': request.GET.get('location'),
            'price__gte': request.GET.get('min_price'),
            'price__lte': request.GET.get('max_price'),
        }

        for filter_key, filter_value in filters.items():
            if filter_value:
                ads = ads.filter(**{filter_key: filter_value})

        return render(request, 'ads/home.html', {'ads': ads[:20]})

class AdDetailView(View):
    def get(self, request, ad_id):
        ad = get_object_or_404(Ad, id=ad_id)
        return render(request, 'ads/ad_detail.html', {'ad': ad, 'car': getattr(ad, 'car', None)})

class CarCreateView(LoginRequiredMixin, View):
    def get(self, request):
        ad_form = AdForm()
        car_form = CarForm()
        image_form = ImageForm()
        inspection_report_form = InspectionReportForm()

        return render(request, 'ads/add_car.html', {
            'ad_form': ad_form,
            'car_form': car_form,
            'image_form': image_form,
            'inspection_report_form': inspection_report_form,
        })

    def post(self, request):
        ad_form = AdForm(request.POST)
        car_form = CarForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)
        inspection_report_form = InspectionReportForm(request.POST)

        if all([ad_form.is_valid(), car_form.is_valid(), image_form.is_valid(), inspection_report_form.is_valid()]):
            ad = ad_form.save(commit=False)
            ad.user = request.user
            ad.save()  
            
            car = car_form.save(commit=False)
            car.ad = ad
            car.save()

            car.save_related_entities(
                car_form=car_form,
                image_form=image_form,
                inspection_report_form=inspection_report_form
            )

            return redirect('ad-list')

        return render(request, 'ads/add_car.html', {
            'ad_form': ad_form,
            'car_form': car_form,
            'image_form': image_form,
            'inspection_report_form': inspection_report_form,
        })
