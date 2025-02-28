from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Company, JobListing, Application

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'name', 'is_verified']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'is_verified', 'verification_token')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('name', 'email')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Company)
admin.site.register(JobListing)
admin.site.register(Application)