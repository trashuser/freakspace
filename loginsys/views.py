# -*- codding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import auth

@csrf_exempt
def login(request):
    if request.user.is_authenticated():
        return redirect('/')
    args = {}
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = 'Користувач не знайдений'
            return render_to_response('loginsys/login.html', args)
    else:
        return render_to_response('loginsys/login.html', args)


def logout(request):
    auth.logout(request)
    return redirect('/')