from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ads.forms import AdForm, CarForm, ImageForm, InspectionReportForm
from ads.models import Ad
from ads.filters import AdFilter
from cars.models import Image, Car


@require_http_methods(["GET"])
def ad_list_view(request):
    ad_filter = AdFilter(request.GET, queryset=Ad.objects.filter(is_active=True))
    return render(request, 'ads/home.html', {'ads': ad_filter.qs[:1000], 'filter': ad_filter})

@require_http_methods(["GET"])
def ad_detail_view(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad, 'car': getattr(ad, 'car', None)})

@login_required
def car_create_view(request):
    if request.method == 'POST':
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

            response = redirect('ad_list')

        else:
            response = render(request, 'ads/add_car.html', {
                'ad_form': ad_form,
                'car_form': car_form,
                'image_form': image_form,
                'inspection_report_form': inspection_report_form,
            })

    else:
        ad_form = AdForm()
        car_form = CarForm()
        image_form = ImageForm()
        inspection_report_form = InspectionReportForm()

        response = render(request, 'ads/add_car.html', {
            'ad_form': ad_form,
            'car_form': car_form,
            'image_form': image_form,
            'inspection_report_form': inspection_report_form,
        })

    return response

@login_required
def user_cars_view(request):
    return render(request, 'ads/user_cars.html', {'ads': Ad.objects.filter(user=request.user, is_active=True)})

@login_required
def car_edit_view(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user, is_active=True)
    car = get_object_or_404(Car, ad=ad, is_active=True)

    if request.method == 'POST':
        ad_form = AdForm(request.POST, instance=ad)
        car_form = CarForm(request.POST, instance=car)
        image_form = ImageForm(request.POST, request.FILES)

        if car.inspection_reports.exists():
            inspection_report_form = InspectionReportForm(request.POST, instance=car.inspection_reports.first())
        else:
            inspection_report_form = InspectionReportForm(request.POST)

        if all([ad_form.is_valid(), car_form.is_valid(), inspection_report_form.is_valid()]):
            ad = ad_form.save()
            car = car_form.save()
            
            if image_form.is_valid():
                car_edit_view_instance = car
                car_edit_view_instance.save_related_entities(car_form, image_form, inspection_report_form)

            messages.success(request, 'Car details updated successfully.')

            response =  redirect('user_cars')

    else:
        ad_form = AdForm(instance=ad)
        car_form = CarForm(instance=car)
        image_form = ImageForm()

        if car.inspection_reports.exists():
            inspection_report_form = InspectionReportForm(instance=car.inspection_reports.first())
        else:
            inspection_report_form = InspectionReportForm()

    response =  render(request, 'ads/edit_car.html', {
                    'ad_form': ad_form,
                    'car_form': car_form,
                    'image_form': image_form,
                    'inspection_report_form': inspection_report_form,
                    'form_instance': ad,
                    'existing_images': car.images.all(),
                })
    
    return response

@login_required
def remove_car_image_view(request, image_id):
    image = get_object_or_404(Image, id=image_id)

    if image.car.ad.user == request.user:
        image.delete()
        messages.success(request, 'Image removed successfully.')
    else:
        messages.error(request, 'You are not authorized to remove this image.')

    return redirect('car_edit', ad_id=image.car.ad.id)

@login_required
def car_delete_view(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)
    ad.is_active = False
    ad.save()
    messages.success(request, 'Car deleted successfully.')
    return redirect('user_cars')
