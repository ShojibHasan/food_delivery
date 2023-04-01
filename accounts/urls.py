from django.urls import path
from . import views
urlpatterns = [
    path('registerUser/',views.registerUser,name='registerUser'),
    path('registerRestaurant/',views.registerRestaurant,name='registerRestaurant'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    
    path('customerDashboard/',views.customerDashboard,name='customerDashboard'),
    path('restaurantDashboard/',views.restaurantDashboard,name='restaurantDashboard'),
    path('myaccounts/',views.myaccount,name='myaccount'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate')
]