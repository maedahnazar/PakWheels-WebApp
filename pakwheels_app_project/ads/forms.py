# forms.py
from django import forms
from ads.models import Ad
from cars.models import Car, Feature, Image, InspectionReport
from django.forms import modelformset_factory

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'price', 'location', 'seller_comments']

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['registered_in', 'color', 'assembly', 'engine_capacity', 'body_type']

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['name']

class InspectionReportForm(forms.ModelForm):
    class Meta:
        model = InspectionReport
        fields = ['inspected_date', 'overall_rating', 'grade', 'exterior_body', 'engine_transmission_clutch', 'suspension_steering', 'interior', 'ac_heater']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['uploaded_image']

ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3, can_delete=True)
