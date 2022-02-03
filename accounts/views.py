from django.shortcuts import redirect, render
from .form import *
from django.contrib.auth import authenticate
from django.contrib.auth import login
from .models import profile


def sign_up(request):
    if request.method == 'POST':
        signup_form = signup(request.POST)
        if signup_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password1')
            signup_form.save()
            user = authenticate(username=username,password = password)
            login(request,user)
            return redirect('/')
    else:
        signup_form = signup()


    return render(request,'accounts/signup.html',{'sign_form':signup_form})


def prof(request):
    data = profile.objects.get(user= request.user)
    print(data)
    context = {'data':data}
    return render(request,'accounts/profile.html',context)


def edit_prof(request):
    data = profile.objects.get(user= request.user)
    if request.method == 'POST':
        profileform = profile_form(request.POST,request.FILES,instance=data)
        userform = user_form(request.POST,instance=request.user)
        if profileform.is_valid() and userform.is_valid():
            profileform.save()
            userform.save()
            return redirect('/accounts/profile')


    else:
        profileform = profile_form(instance=data)
        userform = user_form(instance=request.user)
    context = {"userform":userform,"profileform":profileform}
    return render(request,'accounts/profile-edit.html',context)

