from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Ad


@require_http_methods(["GET"])
def home(request):
    return render(request, 'ads/home.html')

@require_http_methods(["GET"])
def display_ads(request):
    return render(request, 'home.html', {'ads': Ad.objects.all()})

@require_http_methods(["GET"])
def ad_detail(request, ad_id):
    return render(request, 'ads/ad_detail.html', {'ad': get_object_or_404(Ad, id=ad_id)})
