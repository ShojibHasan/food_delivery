from django.contrib import admin
from .models import Restaurant
# Register your models here.

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('user','restaurant_name','restaurant_license','is_approved','created_at')
    list_display_links = ('user','restaurant_name','restaurant_license','is_approved','created_at')

admin.site.register(Restaurant)