from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User as CustomUser

class UserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('username', 'created_at', 'modified_at')

admin.site.register(CustomUser, UserAdmin)
