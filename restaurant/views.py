from django.shortcuts import render

# Create your views here.


def restaurant_profile(request):
    return render(request,'restaurant/restaurant_profile.html')