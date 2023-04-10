from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect
from .forms import RestaurantForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from restaurant.models import Restaurant
# Create your views here.


def restaurant_profile(request):
    profile = get_object_or_404(UserProfile,user = request.user)
    restaurant = get_object_or_404(Restaurant,user = request.user)
    
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        restaurant_form = RestaurantForm(request.POST,request.FILES,instance=restaurant)
        if profile_form.is_valid() and restaurant_form.is_valid():
            profile_form.save()
            restaurant_form.save()
            messages.success(request,'Settings Updated')
            return redirect('restaurant_profile')
        else:
            messages.error(request,"Errors")
    else:
        profile_form = UserProfileForm(instance=profile)
        retaurant_form = RestaurantForm(instance=restaurant)
    
    context={
        'profile_form':profile_form,
        'retaurant_form':retaurant_form,
        'profile':profile,
        'restaurant':restaurant,
    }
    return render(request,'restaurant/restaurant_profile.html',context)