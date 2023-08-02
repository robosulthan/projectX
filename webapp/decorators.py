from django.http import HttpResponseRedirect
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args,**kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('Login')
    return wrapper_func
