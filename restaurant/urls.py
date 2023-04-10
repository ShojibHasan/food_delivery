from django.urls import path,include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('',AccountViews.restaurantDashboard,name='restaurant'),
    path('profile/',views.restaurant_profile,name='restaurant_profile')
]
