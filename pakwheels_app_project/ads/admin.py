from django.contrib import admin

from ads.models import Ad


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'created_at', 'modified_at')
