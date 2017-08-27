from django.shortcuts import render, redirect
from blog import models
from django.views.decorators.csrf import csrf_protect, csrf_exempt
# from datetime import datetime
import time
from .form import *

def out_profile_user(request, id):
    min_5 = 300 # 300 second = 5 min

    update_activity(request)
    if request.user.is_authenticated():
        user = models.UserProfile.objects.get(user_id=request.user.id)
        auth = True
    this_user = models.UserProfile.objects.get(id=id)
    namepage = this_user.user.username
    if request.user.id == id:
        editprofile = True
    if time.time() - this_user.last_activity <= min_5:
        Online = True
    else:
        loctime = time.strftime('%d.%m %H:%M:%S', time.localtime(this_user.last_activity))
    if request.user.is_authenticated():
        auth = True
        if int(request.user.id) == int(id):
            its_me = True
    playlists = models.Playlist.objects.filter(author=this_user)
    posts = models.Post.objects.filter(author=this_user)
    return render(request, 'profileuser/userpage.html', locals())



def edit_profile_user(request, id):
    user = models.User.objects.get(id=id)
    if request.user.is_authenticated() and user == request.user:
        userprofile = models.UserProfile.objects.get(user=user)
        email = userprofile.email
        aboutme = userprofile.about_me
        namepage = 'Змінити профіль ' + user.username
        form = EditUserProfile()

        github = userprofile.pGitHub
        gitlab = userprofile.pGitLab
        linkedin = userprofile.pLinkedIn
        replace = userprofile.pReplace
        facebook = userprofile.pFacebook
        twitter = userprofile.pTwitter
        # todo: area for chages password
        return render(request, 'profileuser/edituserpage.html', locals())
    else:
        return redirect('/auth/login/')


@csrf_protect
def commit_edit_profile_user(request, id):
    if request.POST:
        user = models.UserProfile.objects.get(user=models.User.objects.get(id=id))

        if request.FILES:
            avatar_field = EditUserProfile(request.POST, request.FILES)
            if avatar_field.is_valid():
                userprofile = avatar_field.save(commit=False)
                user.avatar = userprofile.avatar


        email = request.POST.get('email')
        aboutme = request.POST.get('aboutme')

        user.pGitHub = request.POST.get('github')
        user.pGitLab = request.POST.get('gitlab')
        user.pLinkedIn = request.POST.get('linkedin')
        user.pReplace = request.POST.get('replace')
        user.pFacebook = request.POST.get('facebook')
        user.pTwitter = request.POST.get('twitter')

        user.email = email
        user.about_me = aboutme

        user.save()



    return redirect('/user/id'+id)

def update_activity(request):
    if request.user.is_authenticated():
        user = models.UserProfile.objects.get(user_id=request.user.id)
        user.last_activity = time.time()#models.timezone.now()
        user.save(update_fields=['last_activity',])