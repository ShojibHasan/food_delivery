from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import UserForm
from .models import User
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
            
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
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
    