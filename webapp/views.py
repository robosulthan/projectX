from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .forms import *
from .models import *
import urllib.request
import urllib.parse
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
#from .serializers import *
from .tasks import go_to_sleep

# Create your views here.

def home(request):
 	go_to_sleep.delay(6)
        return render(request,'webapp/home.html')


def about(request):
    return render(request,'webapp/about.html')

def contact(request):
    return render(request,'webapp/contact.html')

def Register(request):
    if request.method == 'POST':
        fm = RegisterForm(request.POST)
        if fm.is_valid():
            user = fm.save()
            group = Group.objects.get(name='Vendor')
            user.groups.add(group)
            messages.success(request, 'Account Created Successfully !!')
            return HttpResponseRedirect('/login/')
    else:
        fm = RegisterForm()
        print("Not completed")
    return render(request, 'webapp/register.html', {'form':fm})

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard/')
    else:
        if request.method == "POST":
            fm = LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                print("if part")
                print(uname)
                print(upass)
                user= authenticate(username=uname,password=upass)
                if user is not None:
                    print("nested nested if part")
                    def is_member(user):
                        return user.groups.filter(name='Vendor').exists()
                    ugroup=is_member(user)
                    print(ugroup)
                    login(request, user)
#                    messages.success(request,'You are signin Successfully !!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            print("else part")
            fm = LoginForm()
        return render(request,'webapp/login.html',{'form':fm})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@unauthenticated_user
def dashboard(request):
    return render(request,'webapp/index.html', {'name':request.user.first_name})

@unauthenticated_user
def user_profile(request):
    if request.method == "POST":
        fm = ProfileForm(request.POST, instance=request.user)
        print("Profile inside")
        print(fm)
        if fm.is_valid():
            print("Profile deep inside")
            messages.success(request,'Profile Updated !!!')
            fm.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        print("Profile POST else inside")
        fm = ProfileForm(instance=request.user)
    return render(request, 'webapp/profile.html',{'name':request.user.first_name, 'form':fm})


def change_pwd(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                return HttpResponseRedirect('/profile/')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'webapp/change_pwd.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')
    #---------------------------------------------------------------------------------------------------------------
