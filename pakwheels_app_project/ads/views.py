from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib import messages

from .forms import AdForm, CarForm, ImageForm, InspectionReportForm
from ads.models import Ad
from cars.models import Image, Car
from cars.services import CarService


@require_http_methods(["GET"])
def home(request):
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

@require_http_methods(["GET"])
def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad, 'car': getattr(ad, 'car', None)})

@login_required
def add_car(request):
    if request.method == 'POST':
        ad_form = AdForm(request.POST)
        car_form = CarForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)
        inspection_report_form = InspectionReportForm(request.POST)

        if all([ad_form.is_valid(), car_form.is_valid(), image_form.is_valid(), inspection_report_form.is_valid()]):
            ad = ad_form.save(commit=False)
            CarService.save_ad_with_related(
                ad=ad,
                car_form=car_form,
                image_form=image_form,
                inspection_report_form=inspection_report_form,
                user=request.user
            )
            return redirect('home')

    else:
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
