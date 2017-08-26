# -*- codding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from blog import models


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
            try:
                models.User.objects.get(username=username)
                args['login_error'] = 'Неправильний пароль'
            except:
                args['login_error'] = 'Користувач не знайдений'
            return render_to_response('loginsys/login.html', args)
    else:
        return render_to_response('loginsys/login.html', args)


def logout(request):
    auth.logout(request)
    return redirect('/')

@csrf_exempt
def register (request):
    args = {}
    if request.POST:
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        try:
            models.User.objects.get(username=username)
            args['login_error'] = 'Користувач з таким іменем вже існує'
            # args['username'] = username
            args['email'] = email
            args['password1'] = password1
            args['password2'] = password2

        except:
            newuser_form = UserCreationForm(request.POST)
            print(password1, password2)
            if password1 != password2:
                args['login_error'] = 'Паролі не співпадають'
                args['username'] = username
                args['email'] = email
            elif len(password2) < 8:
                args['login_error'] = 'Довжина паролю повинна бути не менше восьми символів!'
                args['username'] = username
                args['email'] = email
            elif newuser_form.is_valid():
                newuser_form.save()
                newuser = auth.authenticate(username=username, password=password2)
                models.UserProfile(user=newuser, email=email).save()
                auth.login(request, newuser)
                return redirect('/')
            else:
                args['form'] = newuser_form
                args['login_error'] = 'Спробуйте ще раз'
    return render_to_response('loginsys/register.html', args)
