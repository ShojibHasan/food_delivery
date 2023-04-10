from django.shortcuts import redirect, render
from django.contrib import messages,auth
from .forms import UserForm
from .models import User,UserProfile
from restaurant.forms import RestaurantForm
from django.contrib.auth.decorators import login_required
from  .utils import detectUser, send_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from restaurant.models import Restaurant

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
            
            email_subject = "Please active your account"
            email_template = "accounts/emails/account_verification.html"
            send_email(request,user,email_subject,email_template)
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
            
            
            email_subject = "Please active your account"
            email_template = "accounts/emails/account_verification.html"
            send_email(request,user,email_subject,email_template)
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
    
    
def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        messages.error(request,'Invalid Activation link')
        return redirect('home')
    
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
    restaurant = Restaurant.objects.get(user=request.user)
    context ={
        'restaurant':restaurant,
    }
    return render(request,'accounts/restaurant_dashboard.html',context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.get(email=email).exists():
            user = User.objects.get(email__exact=email)
            
            email_subject = "Reset Your Password"
            email_template = "accounts/emails/reset_password_email.html"
            send_email(request,user,email_subject,email_template)
            messages.success(request,'Password Reset Link Has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request,'Account dose not exist')
            return redirect('forgot_password')
    return render(request,'accounts/forgot_password.html')
    
    
def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.info(request,'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request,'Link Expired')
        return redirect('myaccount')
    
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            
            messages.success(request,'Password Reset Successfull')
            return redirect('login')
        else:
            messages.error(request,'Password not matched')
            return redirect('reset_password')
    return render(request,'accounts/reset_password.html')