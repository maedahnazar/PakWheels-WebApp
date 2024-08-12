from django import forms
from django.forms import modelformset_factory

from ads.models import Ad
from cars.models import Car, Image, Feature, Source, InspectionReport


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'price', 'location', 'seller_comments']

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['registered_in', 'color', 'assembly', 'engine_capacity', 'body_type']

    features = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, uploaded_files, initial=None):
        single_file_clean = super().clean

        if isinstance(uploaded_files, (list, tuple)):
            result = [single_file_clean(file, initial) for file in uploaded_files]
        else:
            result = [single_file_clean(uploaded_files, initial)]

        return result

class ImageForm(forms.Form):
    uploaded_images = MultipleFileField()

class InspectionReportForm(forms.ModelForm):
    source = forms.ModelChoiceField(queryset=Source.objects.all(), required=False)

    class Meta:
        model = InspectionReport

        fields = [
            'inspected_date', 'overall_rating', 'grade', 'exterior_body', 
            'engine_transmission_clutch', 'suspension_steering', 
            'interior', 'ac_heater', 'source'
        ]
        
        widgets = {
            'inspected_date': forms.DateInput(attrs={'type': 'date'}),
            'overall_rating': forms.NumberInput(attrs={'step': 0.1}),
            'grade': forms.TextInput(),
            'exterior_body': forms.TextInput(),
            'engine_transmission_clutch': forms.TextInput(),
            'suspension_steering': forms.TextInput(),
            'interior': forms.TextInput(),
            'ac_heater': forms.TextInput(),
            'source': forms.Select(),
        }

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('source'):
            pakwheels_source = Source.objects.get_or_create(name="PakWheels")[0]
            cleaned_data['source'] = pakwheels_source

        return cleaned_data
