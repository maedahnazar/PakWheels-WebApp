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
        
        #ToDO: Remove the slicing and implement pagination
        return render(request, 'ads/home.html', {'ads': ad_filter.qs[:1000], 'filter': ad_filter})


class AdDetailView(View):
    def get(self, request, ad_id):
        ad = get_object_or_404(Ad, id=ad_id, is_active=True)
        car = getattr(ad, 'car', None)

        return render(
                    request, 
                    'ads/ad_detail.html', {
                        'ad': ad,
                        'car': car,
                        'images_exist': car.images.filter(is_active=True).exists(),
                        'images': car.images.filter(is_active=True),
                    }
                )
    

class AdRetrieveCreateView(LoginRequiredMixin, View):
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


class UserCarsListView(LoginRequiredMixin, View):
    def get(self, request):
        ads = Ad.objects.filter(user=request.user, is_active=True)
        return render(request, 'ads/user_cars.html', {'ads': ads})


class AdRetrieveUpdateView(LoginRequiredMixin, View):
    def get(self, request, ad_id):
        ad = get_object_or_404(Ad, id=ad_id, user=request.user, is_active=True)
        car = get_object_or_404(Car, ad=ad, is_active=True)
        
        ad_form = AdForm(instance=ad)
        car_form = CarForm(instance=car)
        image_form = ImageForm()
        inspection_report_form = InspectionReportForm(instance=car.inspection_reports.first() if car.inspection_reports.exists() else None)

        response =  render(request, 'ads/ad_update.html', {
            'ad_form': ad_form,
            'car_form': car_form,
            'image_form': image_form,
            'inspection_report_form': inspection_report_form,
            'ad': ad,
            'active_images': car.images.filter(is_active=True),
        })

    def post(self, request, ad_id):
        ad = get_object_or_404(Ad, id=ad_id, user=request.user, is_active=True)
        car = get_object_or_404(Car, ad=ad, is_active=True)
        
        if 'remove_image_id' in request.POST:
            image_id = request.POST.get('remove_image_id')
            image = get_object_or_404(Image, id=image_id, car=car)
            image.is_active = False
            image.save()

        ad_form = AdForm(request.POST, instance=ad)
        car_form = CarForm(request.POST, instance=car)
        image_form = ImageForm(request.POST, request.FILES)
        inspection_report_form = InspectionReportForm(request.POST, instance=car.inspection_reports.first() if car.inspection_reports.exists() else None)

        if all([ad_form.is_valid(), car_form.is_valid(), image_form.is_valid(), inspection_report_form.is_valid()]):
            ad = ad_form.save()
            car = car_form.save()
            
            car.save_related_entities(
                car_form=car_form,
                image_form=image_form,
                inspection_report_form=inspection_report_form
            )

            messages.success(request, 'Car details updated successfully.')
            response =  redirect('user-cars-list')

        response =  render(request, 'ads/ad_update.html', {
            'ad_form': ad_form,
            'car_form': car_form,
            'image_form': image_form,
            'inspection_report_form': inspection_report_form,
            'ad': ad,
            'active_images': car.images.filter(is_active=True),
        })

        return response


class AdDeleteView(LoginRequiredMixin, View):
    def get(self, request, ad_id):
        ad = get_object_or_404(Ad, id=ad_id, user=request.user)
        ad.is_active = False
        ad.save()

        messages.success(request, 'Car deleted successfully.')

        return redirect('user-cars-list')
