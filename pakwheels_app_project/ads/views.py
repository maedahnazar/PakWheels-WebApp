from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from ads.models import Ad


@require_http_methods(["GET"])
def home(request):
    ads = Ad.objects.all()
    
    if request.GET.get('location'):
        ads = ads.filter(location__icontains=request.GET.get('location'))

    if request.GET.get('min_price'):
        ads = ads.filter(price__gte=request.GET.get('min_price'))

    if request.GET.get('max_price'):
        ads = ads.filter(price__lte=request.GET.get('max_price'))

    return render(request, 'ads/home.html', {'ads': ads})

@require_http_methods(["GET"])
def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad, 'car': getattr(ad, 'car', None)})
