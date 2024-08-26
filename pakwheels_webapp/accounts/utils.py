import json
from django.conf import settings

def load_ads():
    file_path = settings.BASE_DIR / 'pakwheels_ads.json'
    with open(file_path, 'r') as file:
        ads = json.load(file)
    return ads
