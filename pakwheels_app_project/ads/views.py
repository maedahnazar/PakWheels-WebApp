from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Ad


@require_http_methods(["GET"])
def home(request):
    return render(request, 'ads/home.html')

@require_http_methods(["GET"])
def ad_list(request):
    ads = Ad.objects.all()
    return render(request, 'ads/ad_list.html', {'ads': ads})

@require_http_methods(["GET"])
def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})
