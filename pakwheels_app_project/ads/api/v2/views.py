from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from ads.forms import AdForm, CarForm, ImageForm, InspectionReportForm
from ads.models import Ad
from cars.models import Image, Car


class HomeView(View):
    def get(self, request):
        ads = Ad.objects.all()
    
        if request.GET.get('title'):
            ads = ads.filter(title__icontains=request.GET.get('title'))

        if request.GET.get('location'):
            ads = ads.filter(location__icontains=request.GET.get('location'))

        if request.GET.get('min_price'):
            ads = ads.filter(price__gte=request.GET.get('min_price'))

        if request.GET.get('max_price'):
            ads = ads.filter(price__lte=request.GET.get('max_price'))

        return render(request, 'ads/home.html', {'ads': ads[:20]})

class AdDetailView(View):
    def get(self, request, ad_id):
        ad = get_object_or_404(Ad, id=ad_id)
        return render(request, 'ads/ad_detail.html', {'ad': ad, 'car': getattr(ad, 'car', None)})

class AddCarView(LoginRequiredMixin, View):
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
            car = car_form.save(commit=False)  
            car.save_related_entities(
                ad=ad_form.save(commit=False),
                car_form=car_form,
                image_form=image_form,
                inspection_report_form=inspection_report_form,
                user=request.user
            )
            return redirect('home')

        return render(request, 'ads/add_car.html', {
            'ad_form': ad_form,
            'car_form': car_form,
            'image_form': image_form,
            'inspection_report_form': inspection_report_form,
        })
