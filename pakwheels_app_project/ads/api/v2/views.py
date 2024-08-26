from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from ads.forms import AdForm, CarForm, ImageForm, InspectionReportForm
from ads.models import Ad
from ads.filters import AdFilter
from cars.models import Image, Car


class AdListView(View):
    def get(self, request):
        ad_filter = AdFilter(request.GET, queryset=Ad.objects.all())
        return render(request, 'ads/home.html', {'ads': ad_filter.qs[:20], 'filter': ad_filter})

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

            response = redirect('ad-list')
            
        else:
            response = render(request, 'ads/add_car.html', {
                'ad_form': ad_form,
                'car_form': car_form,
                'image_form': image_form,
                'inspection_report_form': inspection_report_form,
            })

        return response
