from django.shortcuts import redirect, render
from django.contrib import messages,auth
from .forms import UserForm
from .models import User,UserProfile
from restaurant.forms import RestaurantForm
from django.contrib.auth.decorators import login_required
from  .utils import detectUser
# Create your views here.


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('home')
    elif request.method == "POST":
        form= UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password,phone_number=phone_number)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,'Your account has been registered successfully')
            return redirect('home')
        else:
            messages.error(request,'Invalid data inpurt')
    else:
        form = UserForm()
    context ={
        'form':form,
    }
    return render(request,'accounts/registerUser.html',context)

def registerRestaurant(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('home')
    elif request.method == "POST":
        form= UserForm(request.POST)
        restaurant_form = RestaurantForm(request.POST,request.FILES)
        if form.is_valid() and restaurant_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password,phone_number=phone_number)
            user.role = User.RESTURANT
            print("Role: ",User.RESTURANT)
            user.save()
            
            restaurant = restaurant_form.save(commit=False)
            restaurant.user = user
            user_profile = UserProfile.objects.get(user=user)
            restaurant.user_profile = user_profile
            restaurant.save()
            messages.success(request,'Your account has been registered successfully')
            return redirect('home')
        else:
            messages.error(request,'Invalid data inpurt')
    else:
        form = UserForm()
        restaurant_form = RestaurantForm()
    context ={
        'form':form,
        'restaurant_form':restaurant_form
    }
    return render(request,'accounts/registerRestaurant.html',context)
    
    
def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are logged in')
            return redirect('myaccount')
        else:
            messages.error(request,'Invalid Login Credentials')
            return redirect('login')
    return render(request,'accounts/login.html')
            
    
def logout(request):
    auth.logout(request)
    messages.info(request,'You are logged out')
    return redirect('login')

@login_required(login_url='login')
def myaccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
def customerDashboard(request):
    return render(request,'accounts/customer_dashboard.html')

@login_required(login_url='login')  
def restaurantDashboard(request):
    return render(request,'accounts/restaurant_dashboard.html')