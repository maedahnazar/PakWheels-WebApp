from django.shortcuts import render, get_object_or_404

from ads.models import Ad


def home(request):
    return render(request, 'ads/home.html', {'ads': Ad.objects.all()})

def ad_detail(request, ad_id):
    return render(request, 'ads/ad_detail.html', {'ad': get_object_or_404(Ad, id=ad_id)})